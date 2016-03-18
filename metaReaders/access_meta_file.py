#!/usr/bin/env python
import os
import fileinput

def read_meta_file(filename, tag):
    for line in fileinput.input(filename):
        if tag == line.strip().split('|')[0].strip():
            fileinput.close()
            return line.strip().split('|')[1].strip()
    return "" #Only returns this if it is not found
    
    
def write_list_meta_file(filename,tags,values=[]):
    #This function deletes all values at the location and writes eack key-value pair
    if(len(values) != 0):
        with open(filename,"w") as file:
            i=0
            while i < len(tags):
                #TODO LOGGER
                #print("tags[%d] = %s, value[%d] = %s" %(i,tags[i],i,values[i]))
                file.write(tags[i] + "| " + values[i]+'\n')
                i=i+1
    else:
        with open(filename,"w") as file:
            i=0
            while i < len(tags):
                file.write(tags[i]+'\n')
                i=i+1