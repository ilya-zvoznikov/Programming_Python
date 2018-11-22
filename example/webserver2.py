from http.server import CGIHTTPRequestHandler, HTTPServer

HTTPServer(('127.0.0.1', 8808), CGIHTTPRequestHandler).serve_forever()
