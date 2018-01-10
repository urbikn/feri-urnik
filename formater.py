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

import extractor as exctr
from lib.course import * 
import sys
import json


# TODO: make anything left of multiple groups
# TODO:  Pls fix spagetti code... PLS!!
# TODO: MAKE COLORS!


class Formater:
    daysSchedual = []  #each entiry represents a new days schedual
    jsonData = None
    groups = []
    classes = None
    classType = None

    def __init__(self, classes, jsonFile):
        self.classes = classes
        self.jsonData = json.load(jsonFile)
        
        groups = self.jsonData["groups"]
        for ID in groups:
            self.groups.append(groups[ID])
    
        # LV -> Laboratorijske vaje
        # SV -> Seminarske vaje
        # RV -> Računalniške vaje
        # SE -> Seminar
        # PR -> Predavanje
        self.classType = ["PR", "UN LV", "UN SV", "UN RV", "UN SE"]


    def __checkGroup(self, course):
        className = course.courseName
        classGroup = course.group
        
        # For students who aren't Erasmus
        if "erasmus" in classGroup.lower():
            return False

        for groupType in self.classType:
            if groupType in classGroup:
                typeGroup = groupType
        
        if "PR" == typeGroup:
            return True
        elif typeGroup in {"UN LV", "UN SV", "UN SE", "UN RV"}:
                groupNumber = int(classGroup.split(typeGroup)[1].strip()[0])
                for group in self.groups:
                    if( group[0] in className.lower() and group[1] == groupNumber):
                        return True
        return False


    def __createCell(self, lenght, data):
        string = "#"
        
        if data in ["#"," ","&","-","=","$"]:
            for i in range(0,lenght):
                string += data

            string = string[:-1] 
        else:
            end = lenght - len(data) - 1
          #  if end % 2 != 0: end += 1 # If the number is odd

            for i in range(0, end):
                if i % 2 == 0:
                    data = "{} ".format(data)
                else:
                    data = " {}".format(data)

            string = "#%s" % data

        return string


    def __makeTable(self, personal=False):
        string = [""]*9 # The height of the table
        day = 0
        date = self.classes[0].date # The date of the first element in list so it can start comparing with others

        for _class_ in self.classes:
            string[0] = "\n\n{}: {}".format(_class_.date, ["PON","TOR","SRE","ČET","PET"][day])

            lenght = _class_.longestStr() + 6 # So it can be proparly formated in the table
            values = ["#"," ", _class_.time, _class_.courseName, _class_.place, _class_.group, " ","#"] # All values needed for a formated "class"
            
            if not personal or self.__checkGroup(_class_):
                # Sees if the schedual changed to a new day
                if(str(date) < str(_class_.date)):

                    # Before it can do anything new, it needs to end the table with "#"
                    for index in range(1,9):
                        string[index] += "#"
                    
                    self.daysSchedual.append(string)
                    string = [""]*9
                    day = day + 1
                    date = str(_class_.date) # Adds new date for different day

                for index in range(1,9):
                    string[index] += self.__createCell(lenght, values[index - 1])

        for index in range(1,9):
            string[index] += "#"

        self.daysSchedual.append(string)





    def createSchedual(self):
        self.__makeTable()        
        self.daysSchedual.append("\n\n\n")
        self.__makeTable(True)        



    def getSchedual(self):
        return self.daysSchedual

# def main(argv=sys.argv):

    # with open("urnik.txt", "w") as file:
        # file.seek(0)
        # file.truncate()
        # for i in output:
            # for j in i:
                # file.write(j + "\n")



if __name__ == "__main__":
    files = open("config/userData.json")
    
    with open("data/data.ics") as file:
        extractor = exctr.Extractor({"UID","DTSTAMP","LOCATION"})
        extractor.extractFromFile(file)
        classes = extractor.getClassList()

    formate = Formater(classes, files)
    formate.createSchedual()
    for i in formate.getSchedual():
        for j in i:
            print(j)

