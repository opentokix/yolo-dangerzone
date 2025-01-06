package main

import (
	"bytes"
	"encoding/json"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/urfave/cli/v2"
)

type Annotation struct {
	Level   string   `json:"level"`
	Invoker string   `json:"invoker"`
	System  string   `json:"system"`
	Stream  string   `json:"stream"`
	Type    string   `json:"type"`
	Message string   `json:"_msg"`
	Tags    []string `json:"tags"`
}

func main() {
	app := &cli.App{
		Name:  "annotation-sender",
		Usage: "Send annotations to VictoriaLogs",
		Flags: []cli.Flag{
			&cli.StringFlag{
				Name:     "invoker",
				EnvVars:  []string{"ANNOTATION_INVOKER", "INVOKER"},
				Required: true,
				Usage:    "Who triggered this command",
			},
			&cli.StringSliceFlag{
				Name:    "tags",
				EnvVars: []string{"ANNOTATION_TAGS", "TAGS"},
				Usage:   "List of tags for the annotation",
			},
			&cli.StringFlag{
				Name:     "message",
				EnvVars:  []string{"ANNOTATION_MESSAGE", "MESSAGE"},
				Required: true,
				Usage:    "The message for the annotation",
			},
			&cli.StringFlag{
				Name:    "token",
				Aliases: []string{"u"},
				EnvVars: []string{"ANNOTATION_TOKEN", "TOKEN"},
				Usage:   "User for elastic search",
			},
			&cli.StringFlag{
				Name:     "type",
				Aliases:  []string{"T"},
				EnvVars:  []string{"ANNOTATION_TYPE", "TYPE"},
				Required: true,
				Usage:    "Type of the annotation",
			},
			&cli.StringFlag{
				Name:    "system",
				Aliases: []string{"s"},
				EnvVars: []string{"ANNOTATION_SYSTEM", "SYSTEM"},
				Value:   "undefined",
				Usage:   "System for elastic search",
			},
			&cli.StringFlag{
				Name:    "host",
				Aliases: []string{"H"},
				EnvVars: []string{"ANNOTATION_HOST", "HOST"},
				Value:   "localhost",
				Usage:   "Host of victorialogs server",
			},
			&cli.StringFlag{
				Name:    "port",
				Aliases: []string{"P"},
				EnvVars: []string{"ANNOTATION_PORT", "PORT"},
				Value:   "443",
				Usage:   "Port of victorialogs server",
			},
			&cli.StringFlag{
				Name:    "scheme",
				EnvVars: []string{"ANNOTATION_SCHEME", "SCHEME"},
				Value:   "https",
				Usage:   "Use http or https",
			},
		},
		Before: func(c *cli.Context) error {
			// Validate type
			validTypes := map[string]bool{
				"warning":     true,
				"ok":          true,
				"error":       true,
				"information": true,
				"critical":    true,
			}
			if !validTypes[c.String("type")] {
				return fmt.Errorf("invalid type: %s", c.String("type"))
			}

			// Validate scheme
			scheme := c.String("scheme")
			if scheme != "http" && scheme != "https" {
				return fmt.Errorf("scheme must be either http or https")
			}

			return nil
		},
		Action: run,
	}

	if err := app.Run(os.Args); err != nil {
		log.Fatal(err)
	}
}

func run(c *cli.Context) error {
	streamFields := "stream,level,invoker,system,type_of"
	uri := fmt.Sprintf("%s://%s:%s/insert/jsonline?_stream_fields=%s",
		c.String("scheme"),
		c.String("host"),
		c.String("port"),
		streamFields,
	)

	annotation := Annotation{
		Level:   "info",
		Invoker: c.String("invoker"),
		System:  c.String("system"),
		Stream:  "annotations",
		Type:    c.String("type"),
		Message: c.String("message"),
		Tags:    c.StringSlice("tags"),
	}

	jsonData, err := json.Marshal(annotation)
	if err != nil {
		return fmt.Errorf("error marshaling JSON: %v", err)
	}

	req, err := http.NewRequest("POST", uri, bytes.NewBuffer(jsonData))
	if err != nil {
		return fmt.Errorf("error creating request: %v", err)
	}

	req.Header.Set("Content-Type", "application/stream+json")
	if token := c.String("token"); token != "" {
		req.Header.Set("Authorization", fmt.Sprintf("Bearer %s", token))
	}

	client := &http.Client{}
	resp, err := client.Do(req)
	if err != nil {
		return fmt.Errorf("error sending request: %v", err)
	}
	defer resp.Body.Close()

	if resp.StatusCode >= 300 {
		return fmt.Errorf("received non-successful status code: %d", resp.StatusCode)
	}

	log.Printf("Log sent successfully: %d", resp.StatusCode)
	return nil
}
