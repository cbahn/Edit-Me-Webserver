#!/usr/bin/env python3

import json
import os.path
from os import path

class DataStore:
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
        self.data.append(element)
    
    def removeAll(self, key, value):
    # The way this is written is not very fast. User beware 🐢.
        newdata = []
        for i in self.data:
            if i[key] != value:
                newdata.append(i)
        self.data = newdata

if __name__ == '__main__':
    d = DataStore('datafiles/example.json')
    
    d.add({"name":"john","id":324})
    d.add({"name":"john","id":882})
    d.add({"name":"fred","id":111})
    d.removeAll('id',111)

    print(d.data)
    d.save()
    