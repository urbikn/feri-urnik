#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    Downloads the data of the URL: http://wise-tt.com/wtt_um_feri/

    The entire download process is done by using Selenium and Firefox

"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import *


import time
import inspect
import os
import sys, getopt
from pathlib import Path

# Used when the main.py process imports this file and this files imports course, filters, ...
path = os.path.realpath(
    os.path.abspath(
        os.path.join(
            os.path.split(
                inspect.getfile(
                    inspect.currentframe()
                )
            )[0],"..")
        )
    )
if path not in sys.path:
    sys.path.insert(0, path)

import downloader.menu as menu

TIME_SLEEP = 2

class Download:
    browser = None
    url = None
    program = None
    year = None
    course = None
    filename = None
    renameFile = None
    profile = webdriver.FirefoxProfile()
    options = Options()
    url = "http://wise-tt.com/wtt_um_feri/"

    isUp = False



    def __init__(self, url=None, downloadPath=None, program=None,year=None, course=None):
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        if downloadPath:
            self.profile.set_preference("browser.download.dir", downloadPath)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                    "application/octet-stream, text/calendar,application/vnd.sus-calendar,text/x-vcalendar")
        self.options.add_argument("--headless")  # Option to hide browser (Comment line to see browser)
        self.browser = webdriver.Firefox(
                firefox_profile=self.profile,
                firefox_options=self.options
                )

        if url: self.url = url
        if program: self.program = program
        if year: self.year = year
        if course: self.course = course
        if downloadPath:
            self.downloadPath = downloadPath
            self.filename = downloadPath + "/calendar.ics"
            self.renameFile = downloadPath + "/data.ics"
        

    def setUp(self):
        """
            Makes a connection to the website.

            If it can't get to the website, it checks the state of internet connection.
            If the connection is OK, it assumes that the URL in self.url is wrong.
        """

        print("""
                     --------------
        Speed of loading the site and of downloading
        the data may differ based on internet
        connection and/or how much their server is loaded.
                     --------------""")

        # Tries to connect to website
        try:
            self.browser.get(self.url)

        except WebDriverException:
            from urllib import error,request
            
            print("""\nError: Cannot connect to website.
                      It's maybe your internet or maybe they changed the URL.
                      Checking!""")
            try:
                request.urlopen("http://google.com") # Google can't go down right
            except error.URLError:
                raise ConnectionError("Tried to connect to google.com. It's your internet.")
            else:
                raise ConnectionRefusedError("Looks like they changed the URL.")

            sys.exit()

        self.isUp = True
 

    def stop(self):
        """
            Kills browser process.
        """
        self.browser.quit()
        self.isUp = False


    def resetSettings(self,program=None,year=None,course=None):
        if program: self.program = program
        if year: self.year = year
        if course: self.course = course


    def __downloadFile(self):
        wait = WebDriverWait(self.browser, 4)
        
        print("Starting to download file")
        time.sleep(TIME_SLEEP)
        
        script = """return $("span:contains('iCal-teden')").parent()["""
        buttonDownloadId = self.browser.execute_script(script + "0].id")
        if buttonDownloadId == "":
            buttonDownloadId = self.browser.execute_script(script + "1].id")

        elementType = wait.until(EC.element_to_be_clickable((By.ID, buttonDownloadId)))
        elementType.click()
 
        # A basic progress bar loop till the file has downloaded
        for i in range(1,10):
            
            # Checks if the file hasn't been downloaded in in the directory self.downloadPath
            if( not any("calendar" in file for file in os.listdir(self.downloadPath)) ):
                time.sleep(0.4)
                sys.stdout.write("\rDownloading {}".format("."*i))
                sys.stdout.flush()
            else:
                print("\nDownloaded file.")
                break

            
            
    def downloadUrnik(self, n=0):
        if n == 3:
            print( "Couldn't download file" )
            return

        wait = WebDriverWait(self.browser, 4)

        # Waits for browser to load website
        wait.until(EC.presence_of_element_located((By.ID, "content")))

        print("Searching for program")
        menu.clickItem(self.browser,0,self.program)
        time.sleep(TIME_SLEEP)
        print("Searching for year")
        menu.clickItem(self.browser,1,self.year)
        time.sleep(TIME_SLEEP)
        print("Searching for course")
        menu.clickItem(self.browser,2,self.course)
            
        self.__downloadFile()
        
        # Checks if downloaded file exists
        if( not any("calendar" in file for file in os.listdir(self.downloadPath)) ):
                print(os.listdir(self.downloadPath))
                print("""\n...
                          Downloaded file doesn't exist
                          Starting new download
                          -------------------------
                       """)
                time.sleep(TIME_SLEEP)
                n += 1
                self.downloadUrnik(n)
                return
            
        os.rename(self.filename, self.renameFile)


if __name__ == "__main__":
    import json
    user_config_file = open('../../config/user_data.json','r')
    user_config = json.loads(user_config_file.read())
    options = user_config['info']


    mainPath = os.path.abspath(os.path.join( os.getcwd(), "../../data")) + '/'
    download = Download(url = "http://wise-tt.com/wtt_um_feri/",
                        program = options['program'],
                        year = options['year'],
                        course = options['course'],
                        downloadPath = mainPath)

    download.setUp()
    download.downloadUrnik()
    download.stop()

