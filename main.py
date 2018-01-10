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
    download = downloader.Download("RIT UN")
    download.setUp()
    download.downloadUrnik()

    print(sys.path)

    with open("data/data.ics") as file:
        print("Start Extracting file")
        extractor = Extractor({"UID","DTSTAMP","LOCATION"})
        extractor.extractFromFile(file)
        
        print("Successfuly extracted file")
        data = extractor.getClassList()

    files = open("config/userData.json")
    
    print("Starting to format raw data")
    formater = Formater(data, files)
    formater.createSchedual()

    print("Writing formated data into file")
    with open("data/urnik.txt", "w") as file:
        file.seek(0)
        file.truncate()
        for i in formater.getSchedual():
            for j in i:
                file.write(j + "\n")
