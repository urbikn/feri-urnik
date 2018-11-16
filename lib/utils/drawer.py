#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

import pathlib
import sys

"""

"""

class Drawer:
    def __init__( self ):
        pass

    def createCell(self, lenght, data):
        string = "#"
        
        if data in ["#"," ","&","-","=","$"]:
            for i in range(0,lenght):
                string += data

            string = string[:-1] 
        else:
            end = lenght - len(data) - 1
            for i in range(0, end):
                if i % 2 == 0:
                    data = "{} ".format(data)
                else:
                    data = " {}".format(data)

            string = "#%s" % data

        return string


    def drawTable(self, classes, num_day ):
        '''
        Gets a list of classes and returns a string of a drawn table that represents the days schedule.
        The function only get's classes for one day, not the whole week!

        '''

        string = [""]*9 # The height of the table

        day = ["PON","TOR","SRE","ČET","PET"][num_day]
        date = classes[0].date.strftime("%d.%m.%Y")
        
        #!! If you change any spacing, you'll need to change urnik.sh !!
        string[0] = "\n\n"
        string[0] += "{}: {}".format( date, day)

        for entiry in classes:
            lenght = entiry.longestStr() + 6 # So it can be proparly formated in the table
            # All values needed for a formated "class"
            values = ["#",
                      " ",
                      entiry.time,
                      entiry.courseName,
                      entiry.place,
                      entiry.group,
                      " ",
                      "#"]

            for index in range(1,9):
               string[index] += self.createCell(lenght, values[index - 1])
        
        # Ends the table
        for index in range(1,9):
            string[index] += "#"

        val = "";
        for value in string:
            val += "\n" + value

        return val

if __name__ == '__main__':
    filename = 'example.ics'
    path = pathlib.Path('../..') / 'test_data' / filename
    if not path.is_file():
        print('File',filename,'doesn\'t exist')
        sys.exit()
    
    
    drawer = Drawer()
    
