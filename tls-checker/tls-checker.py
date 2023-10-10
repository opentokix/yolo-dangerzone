#!/usr/bin/env python3

import socket
import ssl
import click

def check_tls1(host, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1
    context.maximum_version = ssl.TLSVersion.TLSv1
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                return True
    except Exception as e:
        return False

def check_tls1_1(host, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_1
    context.maximum_version = ssl.TLSVersion.TLSv1_1
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                return True
    except Exception as e:
        return False

def check_tls1_2(host, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_2
    context.maximum_version = ssl.TLSVersion.TLSv1_2
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                return True
    except Exception as e:
        return False

def check_tls1_3(host, port):
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    context.minimum_version = ssl.TLSVersion.TLSv1_3
    context.maximum_version = ssl.TLSVersion.TLSv1_3
    context.verify_mode = ssl.CERT_REQUIRED
    context.check_hostname = True
    context.load_default_certs()
    try:
        with socket.create_connection((host, port), timeout=5) as sock:
            with context.wrap_socket(sock, server_hostname=host) as ssock:
                return True
    except Exception as e:
        return False

@click.command()
@click.option('--host', '-h', help='Host to connect to')
@click.option('--port', '-p', default=443, help='Port to connect to')
@click.option('--timeout', '-t', default=5, help='Timeout in seconds')
@click.option('--tls1', is_flag=True, help='Use TLSv1.0')
@click.option('--tls1_1', is_flag=True, help='Use TLSv1.1')
@click.option('--tls1_2', is_flag=True, help='Use TLSv1.2')
@click.option('--tls1_3', is_flag=True, help='Use TLSv1.3')
@click.option('--all', '-a', is_flag=True, help='Check all TLS versions')
def main(host, port, timeout, tls1, tls1_1, tls1_2, tls1_3, all):
    print("Checking TLS versions for host: %s" % host)
    if (( tls1 or all )):
      if check_tls1(host, port):
          print("TLSv1.0 supported")
    if (( tls1_1 or all )):
      if check_tls1_1(host, port):
          print("TLSv1.1 supported")
    if (( tls1_2 or all )):
      if check_tls1_2(host, port):
          print("TLSv1.2 supported")
    if (( tls1_3 or all )):
      if check_tls1_3(host, port):
          print("TLSv1.3 supported")

if __name__ == "__main__":
    main()