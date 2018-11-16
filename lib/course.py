#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

from datetime import datetime

class Course:
    def __init__(self, date = None, time = None, courseName = None, place = None, group = None):
        self.__writeDate(date)
        self.time = time
        self.courseName = courseName
        self.place = place
        self.group = group
    
    def __writeDate(self, date):
        '''
            Date can be written inserted different types.
            Just a quickly written function to work...
            
            return: None
        '''
        
        if date == None:
            pass
        elif str == type(date):
            self.setDateStr(str(date))
        elif datetime == type(date):
            self.setDate(date)
        else:
            print('Couldn\'t write date value (class[0])')
    
    
    def classDuraction(self, start, end):
        '''
            Creates variable self.time to know duraction of class.
            
            return: None
        '''
        hour = []
        for data in [start,end]:
            data= data.split("T")[1][:4]
            data = data[:2] + "." + data[2:]
            hour.append(data)
        
        self.time = "{} - {}".format(hour[0], hour[1])

    def setValues(self, course):
        '''
            Extracts data from list and saves it into object variables.
            
            return: None
        '''
        self.classDuraction(course[0], course[1])
        self.__writeDate(course[0])
        self.courseName = course[2].split(",")[0]
        self.place = " ".join(course[2].split(",")[1:]).lstrip() # slices up words between ",", selects 1-> and joins them together
        self.group = course[3]

    def setDateStr(self, date):
        '''
            Gets date as a string and formats it to be used as datetime.datetime
            object.
            
            return: None
        '''
        
        year = date[0:4]
        month = date[4:6]
        day = date[6:8]

        string = "{}.{}.{}".format(day,month,year)
        self.date = datetime.strptime(string, "%d.%m.%Y")
    
    def longestStr(self):
        '''
            Finds the longest string from all the variables in Course.
        
            return: int
        '''
        
        num = 0
        for i in self.__dict__:
            tmp_num = len(str(self.__dict__[i]))
            if num < tmp_num:
                num = tmp_num

        return num

    def printValues(self):
        for i in self.__dict__.keys():
            print(self.__dict__[i])

