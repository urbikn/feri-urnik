#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

import lib.utils.downloader as downloader
import lib.utils.extractor as extractor
import lib.utils.formater as formater
import lib.course as course
import os, sys, inspect

if __name__ == "__main__":
    download = downloader.Download("RIT UN", "data")  
    download.setUp()
    download.downloadUrnik()
    download.stop()

    with open("data/data.ics") as file:
        print("Start Extracting file")
        extractor = extractor.Extractor({"UID","DTSTAMP","LOCATION"})
        extractor.extractFromFile(file)
        
        print("Successfuly extracted file")
        extrData = extractor.getClassList()

    files = open("config/userData.json")
    
    print("Starting to format raw data")

    if(len(extrData) == 0):
        print("No data to format. Looks like you have a free week.")
        print("Still writting data to file (even thought it's nothing).")
        schedual = None
    else:
        formater = formater.Formater(extrData, files)
        formater.createSchedual()
        print("Writing formated data into file")
        schedual = formater.getSchedual()

    
    with open("data/urnik.txt", "w") as file:
        file.seek(0)
        file.truncate()
        for i in schedual:
            for j in i:
                file.write(j + "\n")
