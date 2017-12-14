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
import extractor as exc
from course import * 
import sys

# This class works specificly with data taken from this site
# URL: https://feri.um.si/urniki5/groups.php

def dude(lengt, data):
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

def main(argv=sys.argv):
   # file = open(dl.download(), "r") # Opens file that was downloaded from the net
    file = open("data.ics", "r")
    
    classList = exc.getCourseData(file)
    
# TODO: zrihti problem z spreminajnem datuma in zraven njenega dneva
# TODO: MAKE COLORS!
    
    output = []
    string = [""]*9
    ina = 0
    date = classList[0].date

    for data in classList[0:len(classList)-1]:
        string[0] ="\n\n" +  data.date + ": {}".format(["PON","TOR","SRE","ČET","PET"][ina])
        lengt = data.longestStr() + 6
        values = ["#"," ", data.time, data.courseName, data.place, data.group, " ","#"]
        if(str(date) < str(data.date)):
            for index in range(1,9):
                string[index] += "#"

            output.append(string)
            string = [""]*9
            ina = ina + 1
            date = str(data.date)

        for index in range(1,9):
            string[index] += dude(lengt, values[index - 1])
    
    for index in range(1,9):
        string[index] += "#"

    output.append(string)
        
    for i in output:
        for j in i:
            print(j)

if __name__ == "__main__":
    main()
