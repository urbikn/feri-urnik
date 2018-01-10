#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    Downloads the data of the URL:  https://feri.um.si/urniki5/groups.php.

"""
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import time
import os
import sys, getopt

class Download:
    browser = None
    course = None
    filename = None
    profile = webdriver.FirefoxProfile()
    options = Options()
    url = "http://wise-tt.com/wtt_um_feri/"



    def __init__(self, course,filename = "../../data/data.ics"):
        self.profile.set_preference("browser.download.folderList", 2)
        self.profile.set_preference("browser.download.manager.showWhenStarting", False)
        self.profile.set_preference("browser.download.dir", os.getcwd() + "/../data")
        self.profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream, text/calendar,application/vnd.sus-calendar,text/x-vcalendar")
        # self.options.add_argument("--headless")
        self.course = course
        self.filename = filename



    def setUp(self):
        self.browser = webdriver.Firefox(firefox_profile=self.profile, firefox_options=self.options)
        self.browser.get(self.url)
 


    def downloadUrnik(self):
        wait = WebDriverWait(self.browser, 4)
        print("Starting click for course.")
        element = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt85_label")))
        element.click()
        print("Clicked course menu.")

        print("\nStarting click for {}.".format(self.course))
        elementType = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt85_6")))
        elementType.click()
        print("Clicked {}.".format(self.course))

        print("\nStarting to download file")
        elementType = wait.until(EC.element_to_be_clickable((By.ID, "form:j_idt151")))
        elementType.click()
        print("\nDownloaded file.")

        time.sleep(2)
        os.rename("../data/calendar.ics", self.filename)

if __name__ == "__main__":
    download = Download("RIT UN")
    download.setUp()
    download.downloadUrnik()
