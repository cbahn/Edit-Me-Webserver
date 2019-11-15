#!/usr/bin/env python3

import json
import os.path
from os import path

class DataStore:
    """
    DataStore is a utiliy for storing and retrieving lists of dictionaries from flat file storage.
    This is meant to emulate a relational database and it is highly suggested, but not enforced, that the 
    dictionaries' keys be the same for each entry. Scalability was not a major consideration and DataStore
    is not reccomended for more than 1000 rows.
    """
    def __init__(self, filename):
        if not filename.endswith('.json'):
            raise NameError("Invalid file name chosen. DataStore filename must end in '.json' .")
        self.filename = filename
        
        if path.exists( filename ):
            self.data = DataStore.__read_data_from_file(filename)
        else:
            self.data = []
            # i'm not sure if an empty file should be created when the DataStore is initialized
            # self.save()
            
    def save(self):
        with open( self.filename, 'w+' ) as f:
            f.write( json.dumps( self.data, indent=2 ) )
            
    def __read_data_from_file( filename ):
        with open(filename) as f:
            return json.loads( f.read() )
    
    def add(self, element):
        # This method will fail if the data is not appendable
        self.data.append(element)
    
    def removeAll(self, key, value):
    # This is not a very fast way of preforming this operation. User beware 🐢.
        newdata = []
        for i in self.data:
            if i[key] != value:
                newdata.append(i)
        self.data = newdata