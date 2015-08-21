#!/usr/bin/env python
import SimpleHTTPServer
import SocketServer

class MyTCPServer(SocketServer.TCPServer):
        allow_reuse_address = True

PORT = 1025
Handler = SimpleHTTPServer.SimpleHTTPRequestHandler


httpd = SocketServer.TCPServer(("", PORT), Handler)

print "Serving at port %d and you didnt forget to export the port?", PORT
httpd.serve_forever()


