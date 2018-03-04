#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

from datetime import datetime

class Course:
    def __init__(self, date = None, time = None, courseName = None, place = None, group = None):
        self.date = date
        self.time = time
        self.courseName = courseName
        self.place = place
        self.group = group

    # What time class starts and ends
    def classDuraction(self, start, end):
        hour = []
        for data in [start,end]:
            data= data.split("T")[1][:4]
            data = data[:2] + "." + data[2:]
            hour.append(data)
        
        self.time = "{} - {}".format(hour[0], hour[1])

    # Extracts data from list and saves it into object variables
    def setValues(self, course):
        self.classDuraction(course[0], course[1])
        self.setDate(str(course[0]))
        self.courseName = course[2].split(",")[0]
        self.place = " ".join(course[2].split(",")[1:]).lstrip() # slices up words between ",", selects 1-> and joins them together
        self.group = course[3]

    # A little better formated date
    def setDate(self, date):
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]

        string = "{}.{}.{}".format(day,month,year)
        self.date = datetime.strptime(string, "%d.%m.%Y")
    
    # Finds the longest string so we know what the widht of the cell must be
    def longestStr(self):
        num = 0
        for i in self.__dict__:
            tmp_num = len(str(self.__dict__[i]))
            if num < tmp_num:
                num = tmp_num

        return num

    def printValues(self):
        for i in self.__dict__.keys():
            print(self.__dict__[i])

