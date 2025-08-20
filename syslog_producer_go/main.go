package main

import (
	"bufio"
	"context"
	"crypto/rand"
	"encoding/hex"
	"errors"
	"flag"
	"fmt"
	"log"
	"net"
	"os"
	"os/signal"
	"strings"
	"syscall"
	"time"
)

// default syslog PRI: facility=1 (user-level), severity=6 (informational) => 14
const defaultPRI = 14

func init() {
	// Configure logger to write to stderr with timestamp
	log.SetOutput(os.Stderr)
	log.SetFlags(log.LstdFlags | log.Lshortfile)
}

func main() {
	if len(os.Args) < 2 {
		usage()
		os.Exit(2)
	}

	protocol := strings.ToLower(os.Args[1])
	udpFlags := flag.NewFlagSet("udp", flag.ExitOnError)
	tcpFlags := flag.NewFlagSet("tcp", flag.ExitOnError)

	var endpoint string
	var rate int
	var appName string

	// shared flags for both subcommands
	addCommonFlags := func(fs *flag.FlagSet) {
		fs.StringVar(&endpoint, "endpoint", "", "host:port of the syslog server")
		fs.IntVar(&rate, "rate", 1, "messages per second (must be positive)")
		fs.StringVar(&appName, "app", "syslog_producer", "APP-NAME field in syslog")
	}
	addCommonFlags(udpFlags)
	addCommonFlags(tcpFlags)

	switch protocol {
	case "udp":
		if err := udpFlags.Parse(os.Args[2:]); err != nil {
			log.Printf("Failed to parse UDP flags: %v", err)
			os.Exit(2)
		}
		log.Printf("Parsed flags: endpoint=%s, rate=%d, app=%s", endpoint, rate, appName)
		if err := run(protocol, endpoint, rate, appName); err != nil {
			log.Printf("UDP run failed: %v", err)
			fmt.Fprintln(os.Stderr, "error:", err)
			os.Exit(1)
		}
	case "tcp":
		if err := tcpFlags.Parse(os.Args[2:]); err != nil {
			log.Printf("Failed to parse TCP flags: %v", err)
			os.Exit(2)
		}
		log.Printf("Parsed flags: endpoint=%s, rate=%d, app=%s", endpoint, rate, appName)
		if err := run(protocol, endpoint, rate, appName); err != nil {
			log.Printf("TCP run failed: %v", err)
			fmt.Fprintln(os.Stderr, "error:", err)
			os.Exit(1)
		}
	case "-h", "--help", "help":
		usage()
		return
	default:
		fmt.Fprintf(os.Stderr, "unknown subcommand %q\n\n", protocol)
		usage()
		os.Exit(2)
	}
}

func usage() {
	fmt.Fprintf(os.Stderr, `Usage:
  syslog_producer udp --endpoint host:port --rate 10 [--app myapp]
  syslog_producer tcp --endpoint host:port --rate 10 [--app myapp]

Sends RFC5424-like syslog lines with a timestamp and random payload at the given rate.
`)
}

func run(protocol, endpoint string, rate int, appName string) error {
	if endpoint == "" {
		return errors.New("--endpoint is required")
	}
	if rate <= 0 {
		log.Printf("Warning: invalid rate %d, defaulting to 1 msg/sec", rate)
		rate = 1
	}

	// Validate protocol
	if protocol != "tcp" && protocol != "udp" {
		return fmt.Errorf("unsupported protocol: %s (must be tcp or udp)", protocol)
	}

	// Validate endpoint format
	if !strings.Contains(endpoint, ":") {
		return fmt.Errorf("invalid endpoint format: %s (expected host:port)", endpoint)
	}

	hostname, err := os.Hostname()
	if err != nil {
		log.Printf("Warning: failed to get hostname: %v, using 'localhost'", err)
		hostname = "localhost"
	}
	pid := os.Getpid()

	log.Printf("Starting syslog producer: protocol=%s, endpoint=%s, rate=%d msg/sec, app=%s", 
		protocol, endpoint, rate, appName)

	ctx, cancel := signal.NotifyContext(context.Background(), syscall.SIGINT, syscall.SIGTERM)
	defer cancel()

	interval := time.Second / time.Duration(rate)
	if interval <= 0 {
		interval = time.Nanosecond // best-effort if rate is extremely high
	}
	ticker := time.NewTicker(interval)
	defer ticker.Stop()

	var conn net.Conn
	var reconnectCount int

	dial := func() (net.Conn, error) {
		log.Printf("Attempting to connect to %s %s", protocol, endpoint)
		return net.Dial(protocol, endpoint)
	}

	conn, err = dial()
	if err != nil {
		return fmt.Errorf("initial dial %s %s failed: %w", protocol, endpoint, err)
	}
	defer func() {
		if conn != nil {
			if err := conn.Close(); err != nil {
				log.Printf("Error closing connection: %v", err)
			}
		}
	}()
	
	log.Printf("Successfully connected to %s %s", protocol, endpoint)

	var writer *bufio.Writer
	if protocol == "tcp" {
		writer = bufio.NewWriter(conn)
	}

	var messageCount int
	lastLogTime := time.Now()

	for {
		select {
		case <-ctx.Done():
			log.Printf("Shutting down gracefully. Sent %d messages total", messageCount)
			if writer != nil {
				if err := writer.Flush(); err != nil {
					log.Printf("Warning: failed to flush buffer during shutdown: %v", err)
				}
			}
			return nil
		case <-ticker.C:
			msg, err := randomHex(16)
			if err != nil {
				log.Printf("Warning: failed to generate random message: %v", err)
				msg = "fallback-message"
			}
			line := formatRFC5424(defaultPRI, time.Now().UTC(), hostname, appName, pid, msg)

			if protocol == "tcp" {
				if _, err := writer.WriteString(line + "\n"); err != nil {
					log.Printf("TCP write error: %v, attempting reconnection", err)
					reconnectCount++
					if conn != nil {
						conn.Close()
						conn = nil
					}
					
					// try to reconnect once per second until context cancelled
					for {
						select {
						case <-ctx.Done():
							return nil
						case <-time.After(time.Second):
							c, e := dial()
							if e == nil {
								conn = c
								writer = bufio.NewWriter(conn)
								log.Printf("TCP reconnection successful (attempt #%d)", reconnectCount)
								break
							} else {
								log.Printf("TCP reconnection failed: %v, retrying in 1s", e)
							}
						}
					}
					continue
				}
				if err := writer.Flush(); err != nil {
					log.Printf("TCP flush error: %v", err)
				}
			} else {
				// UDP
				if _, err := conn.Write([]byte(line)); err != nil {
					log.Printf("UDP write error: %v, attempting reconnection", err)
					reconnectCount++
					if conn != nil {
						conn.Close()
					}
					newConn, dialErr := dial()
					if dialErr != nil {
						log.Printf("UDP reconnection failed: %v", dialErr)
						conn = nil
					} else {
						conn = newConn
						log.Printf("UDP reconnection successful (attempt #%d)", reconnectCount)
					}
				}
			}
			
			messageCount++
			
			// Log progress every 10 seconds
			if time.Since(lastLogTime) >= 10*time.Second {
				log.Printf("Sent %d messages so far", messageCount)
				lastLogTime = time.Now()
			}
		}
	}
}

func randomHex(n int) (string, error) {
	if n <= 0 {
		return "", errors.New("n must be positive")
	}
	b := make([]byte, n)
	if _, err := rand.Read(b); err != nil {
		return "", fmt.Errorf("failed to generate random bytes: %w", err)
	}
	return hex.EncodeToString(b), nil
}

// formatRFC5424 builds a basic RFC5424 syslog message.
// <PRI>1 TIMESTAMP HOST APP PROCID MSGID - MSG
func formatRFC5424(pri int, ts time.Time, host, app string, pid int, msg string) string {
	// Using MSGID "-" (none) and STRUCTURED-DATA "-" for simplicity
	return fmt.Sprintf("<%d>1 %s %s %s %d - %s", pri, ts.Format(time.RFC3339Nano), host, app, pid, msg)
}
