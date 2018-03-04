#! /usr/bin/env python
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    Format the data and saves it to a file.

    This class works specificly with data taken from this site
    URL: https://feri.um.si/urniki5/groups.php
"""

import sys, os, json, inspect, time

# Used when the main.py process imports this file and this files imports course, filters, ...
path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"")))
path1 = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if path not in sys.path:
    sys.path.insert(0, path)
    sys.path.insert(0, path1)

from course import Course
from filters import Filter
from drawer import Drawer

# TODO: make anything left of multiple groups
# TODO:  Pls fix spagetti code... PLS!!
# TODO: MAKE COLORS!


class Formater:
    daysSchedual = []  #each entiry represents a new days schedual
    jsonData = None
    classes = None

    def __init__(self, classes, jsonFile):
        self.classes = classes
        self.jsonData = json.load(jsonFile)


    def __makeTable(self, personal=False):
        '''
        Creates a table of the schedual and returns that in a string.

        Description:
        Arranges 'classes' in 'day' list, each entiry is an list of classes that happen on that day.
            
        '''

        filters = Filter(self.jsonData)
        drawer = Drawer()
        day = []
        day_index = 0
        date = self.classes[0].date # The date of the first element in list so it can start comparing with others
        class_list = []
        

        for entiry in self.classes:
            if not personal or filters.checkGroup(entiry):
                
                # Sees if the schedual changed to a new day
                if(date < entiry.date):
                    day.append( class_list ) 
                    class_list = []
                    date = entiry.date # Adds new date for different day
                
                class_list.append( entiry );
        
        day.append( class_list ) 
        string = ""
        for index, value in enumerate(day):
            string += drawer.drawTable(value, index)

        self.daysSchedual.append(string)



    def createSchedual(self):
        self.__makeTable()        
        self.daysSchedual.append("\n\n\n")
        self.__makeTable(True)        

    
    def createDummySchedual(self):
        self.__makeTable()        
        self.daysSchedual.append("\n\n\n")
        self.__makeTable()        

    def getSchedual(self):
        return self.daysSchedual




if __name__ == "__main__":
    from extractor import Extractor

    mainPath = os.path.abspath(os.path.join( os.getcwd() , "../../"))

    jsonPath = os.path.join(mainPath, "config", "userData.json")
    files = open(jsonPath)
    
    calendarPath = os.path.join(mainPath, "data", "data.ics")

    with open(calendarPath) as file:
        extractor = Extractor({"UID","DTSTAMP","LOCATION"})
        extractor.extractFromFile(file)
        classes = extractor.getClassList()
        
    dummyClass = False
    if( len(classes) == 0 ):
        print("\nThe extractor returned an empty list.")
        print("The program didn't have any data to extract.")
        print("No data to format.")
        classes = extractor.getDummyList()
        dummyClass = True
    
    formate = Formater(classes, files)

    if( dummyClass ):
        formate.createDummySchedual()
    else:
        formate.createSchedual()

    for i in formate.getSchedual():
        print(i)

