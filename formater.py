#! /usr/bin/env python
# -*- coding: utf-8 -*-
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

import downloader as dl
import extractor as exctr
from course import * 
import sys

# This class works specificly with data taken from this site
# URL: https://feri.um.si/urniki5/groups.php

groups = [ # Only fix this is the university is retarded
        [
            ["angleščina", 1],
            ["matematika", 1]
        ],
        ["programi", 3],
        ["spleta", 3],
        ["oprema", 3]
]

output = [] # Had to make it global, because passing a variable in function doesn't work. Fuck.
            # Oh and each entiry represents a new days schedual


# TODO: make anything left of multiple groups
# TODO:  Pls fix spagetti code... PLS!!

def checkGroup(course):
    name = course.courseName
    group = course.group
    
    if "PR" in group: # The class isn't a group but a regular lecture
        return True

    elif groups[0][0][0].upper() in name : # Course is english
        group_data = ((group.split("UN SE")[1]).split(",")[0]).lstrip()[0] # Long story short, it just gets the number of the group
        if groups[0][0][1] == int(group_data): # If groups is the same
            return True

    elif groups[0][1][0].upper() in name : # Course is Math
        if "UN LV" in group:
            typeGroup = "UN LV"
        else:
            typeGroup = "UN SV"
        group_data = ((group.split(typeGroup)[1]).split(",")[0]).lstrip()[0] # Long story short, it just gets the number of the group
        if groups[0][1][1] == int(group_data): # If groups is the same
            return True

    elif "RV" in group:
        try:
            group_data = group.split("RV")[2].lstrip()[0]
            for crs in groups[1:]:
                if crs[0].upper() in name:
                    if crs[1] == int(group_data):
                        return True
        except:
            print("fail")

    return False

def createCell(lengt, data):
    string = "#"
    
    if data in ["#"," ","&","-","=","$"]:
        for i in range(0,lengt):
            string += data

        string = string[:-1] 
    else:
        end = lengt - len(data) - 1
      #  if end % 2 != 0: end += 1 # If the number is odd

        for i in range(0, end):
            if i % 2 == 0:
                data = "{} ".format(data)
            else:
                data = " {}".format(data)

        string = "#%s" % data

    return string

def makeTable(classes, entire):
    string = [""]*9 # The height of the table
    day = 0
    date = classes[0].date # The date of the first element in list so it can start comparing with others

    for _class_ in classes[ 0:len(classes) - 1 ]:
        string[0] = "\n\n{}: {}".format(_class_.date, ["PON","TOR","SRE","ČET","PET"][day])

        length = _class_.longestStr() + 6 # So it can be proparly formated in the table
        values = ["#"," ", _class_.time, _class_.courseName, _class_.place, _class_.group, " ","#"] # All values needed for a formated "class"
        
        if entire:
            # Sees if the schedual changed to a new day
            if(str(date) < str(_class_.date)):

                # Before it can do anything new, it needs to end the table with "#"
                for index in range(1,9):
                    string[index] += "#"
                
                output.append(string)
                string = [""]*9
                day = day + 1
                date = str(_class_.date) # Adds new date for different day

            for index in range(1,9):
                string[index] += createCell(length, values[index - 1])
        elif checkGroup(_class_):
            # Sees if the schedual changed to a new day
            if(str(date) < str(_class_.date)):

                # Before it can do anything new, it needs to end the table with "#"
                for index in range(1,9):
                    string[index] += "#"
                
                output.append(string)
                string = [""]*9
                day = day + 1
                date = str(_class_.date) # Adds new date for different day

            for index in range(1,9):
                string[index] += createCell(length, values[index - 1])

    for index in range(1,9):
        string[index] += "#"

    output.append(string)

def main(argv=sys.argv):
   # file = open(dl.download(), "r") # Opens file that was downloaded from the net
    file = open("data.ics", "r")
    
    classes = exctr.getCourseData(file)
    
# TODO: MAKE COLORS!
    
    makeTable(classes, True)
    output.append("\n\n\n")
    makeTable(classes, False)

    with open("urnik.txt", "w") as file:
        file.seek(0)
        file.truncate()
        for i in output:
            for j in i:
                file.write(j + "\n")

if __name__ == "__main__":
    main()
