#!/usr/bin/env python3

# Based Largely off of https://gist.github.com/mdonkers/63e115cc0c79b4f6b8b3a6b797e485c7

# Import Python modules we're going to use
from http.server import BaseHTTPRequestHandler, HTTPServer
from string import Template
from urllib.parse import parse_qs
import logging
import random
import html

# Import the DataStore.py functions
from DataStore import DataStore

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

# Location of the guestlist storage file
guestlist_file_location = 'datafiles/guestlist.json'

message_of_the_day = "This message of the day is brought to you by templating."

#####################
###  DEFINITIONS  ###
#####################

def homepage_builder():
    filein = open( 'index.html' )
    templ = Template( filein.read() )
    result = templ.substitute( {'motd': message_of_the_day, 'table':NameBook().generate_table()} )
    return result

class NameBook:
    # The guestlist stores the list of all names and is automatically backed up to the guestlist_file_location file
    guestlist = DataStore( guestlist_file_location )
    
    def add_guest(self, new_name):
        # IDs are assigned randomly. They don't really surve any purpose except adding a second value to each name
        new_id = random.randrange(1000000)
        self.guestlist.add( {'name': new_name, 'id': new_id } )
        self.guestlist.save() # save after each guest is added
        

    def generate_table(self):
        result = "" 
        for i in self.guestlist.data:
            name_to_show = html.escape( str( i['name'] ) )
            id_to_show = html.escape( str(i['id']) )
            result += "<tr><td>{name}</td><td class='number'>{id}</td></tr>".format( name=name_to_show, id=id_to_show )
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
        
        # If the request is for the main page then we generate the page using the homepage_builder function
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(homepage_builder().encode('utf-8'))
        
        # If the response is asking for the style.css file or the favicon.ico file then respond with the file
        elif self.path == '/res/style.css':
            self.__send_file('res/style.css','text/css')
            
        elif self.path == '/res/favicon.ico':
            self.__send_file('res/favicon.ico','image/x-icon')
            
        else: # If the response isn't recognized, send a 404 file not found error
            self.send_response(404)
            self.end_headers()


    def do_POST(self):
        """ If a POST request is received, then we have new data we want to add to the list.
        More info on GET vs POST https://www.w3schools.com/tags/ref_httpmethods.asp """
        
        # The only valid path is /guestlist. Reject everything else with a 404 error
        if self.path == '/guestlist':
        
            # Parse the post form data and put it in post_fields
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            # Thanks to https://stackoverflow.com/a/31363982 for info on how to parse POST form data
            post_fields = parse_qs(post_data, strict_parsing=True)
            
            logging.info("POST request, Path: %s, Body:\n%s\n",str(self.path), str(post_fields))
        
            # Add the new name to the guestlist
            # The [0] at the end is nessesary because the parse_qs creates a list of responses in case there are identical 'name' fields
            NameBook().add_guest( post_fields['name'][0] )
            
            # Once the post request has been processed, use a 303 redirect to send the browser back to '/'
            # wikipedia.org/wiki/Post/Redirect/Get
            self.send_response(303)
            # self.send_header('Content-type', 'text/html') # I don't think I need this for a 303 redirect
            self.send_header('Location', '/')
            self.end_headers()
        else:
            self.send_response(404)
            self.end_headers()
        
        
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