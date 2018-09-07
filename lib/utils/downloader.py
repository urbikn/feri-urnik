#! /usr/bin/env python
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
import os
import sys, getopt
from pathlib import Path

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



    def __init__(self, url, downloadPath, program,year=None, course=None):
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.dir", downloadPath)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                                    "application/octet-stream, text/calendar,application/vnd.sus-calendar,text/x-vcalendar")
        # self.options.add_argument("--headless")  # Option to hide browser (Comment out to see browser)
        self.browser = webdriver.Firefox(firefox_profile=self.profile,
                                         firefox_options=self.options)
        self.url = url
        self.program = program
        self.year = year
        self.course = course
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
            import urllib
            print("""\nError: Cannot connect to website.
                      It's maybe your internet or maybe they changed the URL.
                      Checking!""")
            try:
                urllib.request.urlopen("http://google.com") # Google can't go down right
            except urllib.error.URLError:
                print("Tried to connect to google.com. It's your internet.")
            else:
                print("Looks like they changed the URL.")

            sys.exit()
 

    def stop(self):
        """
            Kills browser process.
        """
        self.browser.quit()


    def __clickDropdown(self, program=None, year=None, course=None):
        """
            Finds the dropdown menu of program/year/course and clicks it to generate
            the programs/year/course list of options.
            After that it just clicks the option specified
            
            Default is 'program'.
        """
    
        wait = WebDriverWait(self.browser, 4)
        
        # Figures out which dropdown menu you mean to access
        if year:
            values = {'name':'year','data': self.year,'dropdown_num': 1}
            
        elif course:
            values = {'name':'course','data': self.course, 'dropdown_num': 2}
            
        else:
            values = {'name':'program','data': self.program,'dropdown_num':0}
        
        print("Starting to find dropdown of {}.".format(values['name']))
        
        # Not using jquery to execute the click instead use Selenium, so it can fully load
        script ="return $('.noBorderBasicTable:eq(1) label:eq({})').get()[0].id.match(/\d+/)[0]".format(values['dropdown_num'])
                
        tagID = "form:j_idt" + self.browser.execute_script(script)
        element = wait.until(EC.presence_of_element_located((By.ID, tagID + "_label")))
        element.click()

        time.sleep(1)
        
        # Finds the specific option based on 'data' in values
        print("Starting click for",values['name'] + ':', values['data'])
        script = """return $(document.getElementById('{0}')).find("li[data-label='{1}']")[0].id
                """.format(tagID+'_items',values['data'])
        ID = self.browser.execute_script(script)
        elementType = wait.until(EC.presence_of_element_located((By.ID, ID )))
        elementType.click()
        

    def __downloadFile(self):
        wait = WebDriverWait(self.browser, 4)
        
        print("Starting to download file")
        time.sleep(1)
        
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

        self.__clickDropdown(program=True)
        if year: # if year is specified
            self.__clickDropdown(year=True)
        if course: # if course is specified
            self.__clickDropdown(course=True)
            
        self.__downloadFile()
        
        # Checks if downloaded file exists
        if( not any("calendar" in file for file in os.listdir(self.downloadPath)) ):
                print(os.listdir(self.downloadPath))
                print("""\n...
                          Downloaded file doesn't exist
                          Starting new download
                          -------------------------
                       """)
                time.sleep(1)
                n += 1
                self.downloadUrnik(n)
                return
            
        os.rename(self.filename, self.renameFile)


if __name__ == "__main__":
    mainPath = os.path.abspath(os.path.join( os.getcwd(), "../../data")) + '/'
    download = Download(url = "http://wise-tt.com/wtt_um_feri/",
                        program = "RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE UN (BU20)",
                        year = 1,
                        course = "RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE (BU20)"
                        downloadPath = mainPath)

    download.setUp()
    download.downloadUrnik()
    download.stop()

