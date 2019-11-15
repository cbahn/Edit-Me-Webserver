#!/usr/bin/env python3

# Based Largely off of https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7

# This is an include statement. It tells python that it should load up
# the functions for HTTPServer, Template, and logging because we're going to use them
from http.server import BaseHTTPRequestHandler, HTTPServer
from string import Template
from urllib.parse import parse_qs
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
    
    def __send_file(self,file_location,content_type):
            with open(file_location, 'rb') as file:            # Using 'with' ensures that the file is closed once we're done
                self.send_response(200)                        # Response type: Success 👍
                self.send_header('Content-type', content_type) # Set an appropriate Content-type
                self.end_headers()                             # This line is important for separing the headers from the response
                self.wfile.write(file.read())                  # Write the file data directly to the response

    def do_GET(self):
        """ When a GET request is received, we want to examine the url to determine what to do with it.
        The self.path variable stores the request path. For instance, if the browser navigates to 
        http://localhost:8080/images then the path will be '/images'.
        """
        # If the request is for the main page then we generate the page using the page_builder function
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(page_builder().encode('utf-8'))
        
        # If the response is asking for the style.css file or the favicon.ico file then respond with the file
        elif self.path == '/res/style.css':
            self.__send_file('res/style.css','text/css')
            
        elif self.path == '/res/favicon.ico':
            self.__send_file('res/favicon.ico','image/x-icon')
            
        else: # If the response isn't recognized, send a 404 file not found error
            self.send_response(404)
            self.end_headers()

# wikipedia.org/wiki/Post/Redirect/Get

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        # Thanks to https://stackoverflow.com/a/31363982 for info on how to parse POST form data
        post_fields = parse_qs(post_data, strict_parsing=True)
        
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                str(self.path), str(self.headers), post_fields)

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
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