#!/usr/bin/env python3

# Based Largely off of https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7

# This is an include statement. It tells python that it should load up
# the functions for HTTPServer, Template, and logging because we're going to use them
from http.server import BaseHTTPRequestHandler, HTTPServer
from string import Template
import logging

##################
###  SETTINGS  ###
##################

# The port is the part put after the colon in the URL. Example  localhost:8080/pictures
# The browser will default to 80 otherwise
port=8080

# This determines how much info is displayed to the console window after each request
#  - logging.INFO      every request will be logged
#  - logging.WARNING   only requests that fail and errors will be logged
#  - logging.CRITICAL  no logs except if the program crashes
logging_level = logging.INFO


#####################
###  DEFINITIONS  ###
#####################

def create_table():
    data = [
        {'name':'Judy', 'id':385927},
        {'name':'Brian', 'id':239429},
        {'name':'Kendric', 'id':111903}]
    result = ""
    for i in data:
        result += '<tr><td>{name}</td><td>{id}</td></tr>'.format( name=i['name'], id=i['id'] )
    return result


def page_builder():
    filein = open( 'index.html' )
    templ = Template( filein.read() )
    result = templ.substitute( {'name':'Bobby Hill','table':create_table()} )
    return result


class Request_handler(BaseHTTPRequestHandler):
    def _set_200_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
    
    def _set_400_response(self):
        self.send_response(400)
        self.end_headers()

    def do_GET(self):
        logging.info("GET request,\nPath: %s\n", str(self.path))
        
        ## NEXT STEPS: add stuff to load the res properly
        # Also, the post request should start redirecting correctly
        
        if self.path == '/':
            self._set_200_response()
            self.wfile.write(page_builder().encode('utf-8'))
        elif self.path == '/res/style.css':
            pass
        else:
            self._set_400_response()

# wikipedia.org/wiki/Post/Redirect/Get

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_data.decode('utf-8'))

        self._set_200_response()
        self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        
##############
###  MAIN  ###
##############
# This is the 'main' part of the program. It is the first thing run when the program is started

if __name__ == '__main__':
    # Turn on logging so that info appears in the console window
    logging.basicConfig(level=logging_level)
    
    # Start the webserver listening at our home address and port
    # Request_handler will be responsible for all requests
    server_address = ('', port)
    httpd = HTTPServer(server_address, Request_handler)
    logging.info('Starting webserver on localhost:{} ...\n'.format(port))

    # For now the only way to exit the server is by ending the process
    httpd.serve_forever()