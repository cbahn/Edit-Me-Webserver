#!/usr/bin/env python3

# This is an include statement. It tells python that it should load up
# the functions for HTTPServer and logging because we're going to use them
from http.server import BaseHTTPRequestHandler, HTTPServer
import logging

##################
###  SETTINGS  ###
##################

# The port is the part put after the colon in the URL. Example  localhost:8080/pictures
# The browser will default to 80 if you don't put one in the URL
port=8080

#####################
###  DEFINITIONS  ###
#####################

class Request_handler(BaseHTTPRequestHandler):
    def set_200_response_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self.set_200_response_headers()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        
##############
###  MAIN  ###
##############

# This is the 'main' part of the program. When you start the program this is the first thing that gets run.
if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = HTTPServer(server_address, Request_handler)
    logging.info('Starting webserver on localhost:{} ...\n'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')