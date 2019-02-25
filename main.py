#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

import lib.downloader.downloader as downloader
import lib.downloader.menu as menu
import lib.utils.extractor as extractor
import lib.utils.formater as formater
import lib.utils.filters as filters
import lib.utils.drawer as drawer
import lib.config.main as config
import lib.course as course

import os, sys, inspect, time, getopt, json, datetime
import atexit
from pathlib import Path

url = 'http://wise-tt.com/wtt_um_feri/'
browser_up = False
user_data = None

def clean_on_exit(browser ):
    '''
    shuts down the browser and cleans any unneeded data
    '''

    if browser != None:
        if browser.isUp:
            browser.stop()


def checkDownloadTime():
    '''
    Checks if the calendar was downloaded this week. If not, saves new week in process_data.json and returns True.
    '''

    week = datetime.datetime.now().isocalendar()[1]
    path = Path.cwd() / 'config' / 'process_data.json'

    with path.open() as file:
        data = json.load(file)
    
    if( data["week"] < week  ):
        
        data["week"] = week
        with path.open('w') as file:
            json.dump(data, file)

        return True

    return False

def startBrowser():
    global user_data
    user_data = Path.cwd() / 'config' / 'user_data.json'
    json_user_data = None
    if not user_data.is_file():
        print('File','user_data.json','doesn\'t exist')
        sys.exit()
    else:
        user_data_json = json.load(user_data.open())

    downloadPath = os.path.abspath(os.path.join( os.getcwd(), "data"))
    download = downloader.Download(url=url,
                                   downloadPath=downloadPath,
                                   program=user_data_json['info']['program'],
                                   year=user_data_json['info']['year'],
                                   course=user_data_json['info']['course'])  
    download.setUp()
    global browser_up
    browser_up = True
    return download


def restartSettingsInDownload(download):
    user_data_json = json.load(user_data.open())
    download.resetSettings(program=user_data_json['info']['program'],
                           year=user_data_json['info']['year'],
                           course=user_data_json['info']['course'])  
    return download


if __name__ == "__main__":
    download = None


    if 'reconfig' in sys.argv[1:]:
        print("Time to reconfig")
        download = startBrowser()
        atexit.register(clean_on_exit, download);
        for i in range(3):
            config.change(i,download.browser,True)
            time.sleep(1)
        if 'force_download' not in sys.argv[1:]:
            sys.exit()

    # Check if it wasn't a force run ( so not manually wanting to download data )
    if "force_download" not in sys.argv[1:]:
        print("can't download")
        if( not checkDownloadTime() ):
            sys.exit()

    print("\n\t---- Downloading ----" )
    if not browser_up:
        download = startBrowser()

    atexit.register(clean_on_exit, download);
    download.downloadUrnik()

    print("\n\t---- Extraction ----" )
    with open("data/data.ics") as file:
        print("Start Extracting file")
        extractor = extractor.Extractor({"UID","DTSTAMP","LOCATION"})
        extractor.extractFromFile(file)
        
        print("Successfuly extracted file")
        extrData = extractor.getClassList()


    time.sleep(1)
    print("\n\t---- Formatting ----" )
    errorStr = ""
    extrctDummy = False
    print("Starting to format raw data")
    
    if(len(extrData) == 0):
        print("\n\n=====\nNo data to format. Looks like you have a free week.\n=====\n\n")
        errorStr = " (even thought it's nothing)."
        extrData = extractor.getDummyList()
        extrctDummy = True
        sys.exit(0)
    
    formater = formater.Formater(extrData, user_data.open())

    if(extrctDummy):
        formater.createDummySchedual()
    else:
        formater.createSchedual()

    schedule = formater.getSchedual()

    time.sleep(1)
    print("\n\t---- Writting to file ----" )
    print("Writing formated data into file" + errorStr)
    
    with open("data/urnik.txt", "w") as file:
        file.seek(0)
        file.truncate()
        for i in schedule:
            file.write(i + "\n")
    
    print("\n\t---- Finished ----" )
