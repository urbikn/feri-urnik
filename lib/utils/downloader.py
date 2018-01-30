#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    Downloads the data of the URL: http://wise-tt.com/wtt_um_feri/

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

class Download:
    browser = None
    course = None
    filename = None
    renameFile = None
    profile = webdriver.FirefoxProfile()
    options = Options()
    url = "http://wise-tt.com/wtt_um_feri/"



    def __init__(self, course, downloadPath = "../../data/"):
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.dir", downloadPath)
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream, text/calendar,application/vnd.sus-calendar,text/x-vcalendar")
        # self.options.add_argument("--headless")  # Option to hide browser
        self.course = course
        self.filename = downloadPath + "calendar.ics"
        self.renameFile = downloadPath + "data.ics"




    def setUp(self):
        try:
            self.browser = webdriver.Firefox(firefox_profile=self.profile, firefox_options=self.options)
            self.browser.get(self.url)
        except WebDriverException:
            import urllib
            print("\nError: Cannot connect to website. turn on your shitty internet or maybe they changed the URL.\nInvestigating this crap...\n")

            try:
                urllib.request.urlopen("http://google.com") # Google can't go down right
            except urllib.error.URLError:
                print("Fix your shitty network connection!")
            else:
                print("Yup, they changed the URL!")

            sys.exit()
 

    def stop(self):
        self.browser.quit()

    def downloadUrnik(self):
        wait = WebDriverWait(self.browser, 4)

        # Waits for browser to load
        wait.until(EC.presence_of_element_located((By.ID, "content")))

        print("Starting click for course.")
        numberId = self.browser.execute_script("return $('.noBorderBasicTable')[1].children[0].children[1].children[0].children[0].children[2].id.match(/\d+/)[0]")

        element = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt"+ numberId +"_label")))
        element.click()
        print("Clicked course menu.")

        print("\nStarting click for {}.".format(self.course))
        elementType = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt"+ numberId +"_6")))
        elementType.click()
        print("Clicked {}.".format(self.course))

        print("\nStarting to download file")
        buttonDownloadId = self.browser.execute_script("return $(\"span:contains('iCal-teden')\").parent()[1].id")

        
        elementType = wait.until(EC.element_to_be_clickable((By.ID, buttonDownloadId)))
        elementType.click()
        print("\nDownloaded file.")

        time.sleep(2)
 #       os.rename(self.filename, self.renameFile)

if __name__ == "__main__":
    download = Download("RIT UN")
    download.setUp()
    download.downloadUrnik()
    download.stop()
