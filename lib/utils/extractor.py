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

import sys, os, json, inspect

path = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"..")))
if path not in sys.path:
    sys.path.insert(0, path)

from course import Course

# returns list of every occuring class in week
class Extractor:
    __classList = None
    __unwantedLines = None

    def __init__(self, unwanted):
        self.__unwantedLines = unwanted
        self.__classList = []

    # Removes entries in list based on what the unwanted lines
    # the user suggested
    def __rmEntries(self, list):
        for index, data in enumerate(list):
            for unwanted in self.__unwantedLines:
                if unwanted in data:
                    del list[index]

        list = self.__rmUnwantedChar(list)

        # Location doesn't want to be found, so I bruteforce removed it
        for i in self.__unwantedLines:
            if "LOC" in i:
                return list[1:]
        
        return list

    # Removes left of ":" and whitespaces between entire text
    def __rmUnwantedChar(self, list):
        tmpList = []
        
        for entiry in list:
            entiry = entiry.split(":")[1].strip()
            tmpList.append(entiry)

        return tmpList

    def getClassList(self):
        return self.__classList
    

    def extractFromFile(self, file):
        for index, line in enumerate(file):
            # initialize variables and list 
            if "BEGIN:VEVENT" in line:
                course = []

            elif "END:VEVENT" in line:
                # Removes the lines that shouldn't be in list
                tmp = self.__rmEntries(course)
                data = Course()
                data.setValues(tmp)
                self.__classList.append( data )

                pass

            else:
                try:
                    # Fuck newlines
                    course.append(line.strip("\n"))
                except:
                    pass


if __name__ == "__main__":
    with open("../../data/data.ics") as file:
        extractor = Extractor({"UID","DTSTAMP","LOCATION"})
        extractor.extractFromFile(file)
        extractor.getClassList()[0].printValues()


