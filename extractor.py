#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    Extracts the data from the downloaded file
"""
import downloader as dl
from course import *
import sys

# Removes unwanted characters
def removeUnwantedCharacters(list):
    tmp_test = []
    for data in list:
        # Gives back everything right of the ":" character
        data = data.split(":")[1]
        
        # Removes whitespace left and right of string
        data = data.rstrip().lstrip()
        tmp_test.append(data)
    
    return tmp_test

# Removes data specified params
def removeListData(list, params):
    for index, data in enumerate(list):
        for unwantedData in params:
            if unwantedData in data:
                del list[index]

    list = removeUnwantedCharacters(list)

    # Location doesn't want to be found, so I bruteforce remove it
    for i in params:
        if "LOC" in i:
            return list[1:]
    
    return list


# returns list of every occuring class in week
def getCourseData(file):   
    classList = [] # List of 

    for count, line in enumerate(file):
        # initialize variables and list 
        if "BEGIN:VEVENT" in line:
            course = []

        elif "END:VEVENT" in line:
            # Removes the lines that shouldn't be in list
            tmp = removeListData(course, {"UID","DTSTAMP","LOCATION"}) 
            data = Course()
            data.setValues(tmp)
            classList.append( data )

        else:
            try:
                # Fuck newlines
                course.append(line.strip("\n"))
            except:
                pass

    return classList
