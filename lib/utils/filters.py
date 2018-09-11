#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""

"""

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
        self.classType = ["PR", "UN LV", "SV", "UN RV", "UN SE"]


    def checkGroup(self, course):
        '''
        
        
        return: True/False
        '''
        
        className = course.courseName
        classGroup = course.group
        
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
