#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""

"""

import re

class Filter:
    groups = []
    classType = None

    def __init__( self, jsonData ):
        groups = jsonData["groups"]
        for ID in groups:
            self.groups.append(groups[ID])
        
        # LV -> Laboratorijske vaje
        # SV -> Seminarske vaje
        # RV -> Računalniške vaje
        # SE -> Seminar
        # PR -> Predavanje
        self.classType = ["PR"]

        self.workType =  [ "LV","SV", "SE", "RV"]
        tmp = []
        for i in self.workType:
            tmp.append( "VS " + i )
            tmp.append( "UN " + i )

        self.workType.extend(tmp)

        self.classType.extend( self.workType )


    def checkGroup(self, course):
        '''
        
        
        return: True/False
        '''
        
        typeGroup=None
        className = course.courseName
        classGroup = course.group
        
        if "erasmus" in classGroup.lower():
            return False

        test = classGroup.replace(',','').strip()
        for groupType in self.classType:
            if groupType in test:
                typeGroup = groupType
        
        if "PR" == typeGroup:
            return True
        elif typeGroup in self.workType:
                data = re.search(typeGroup+'\d', classGroup).group();

                # Regex didn't find any group with a number
                if data == None:
                    return True 

                groupNumber = int(data[-1])
                for group in self.groups:
                    if group[0] in className.lower() and ( group[1] == groupNumber or group[1] == 0):
                        return True
        return False
