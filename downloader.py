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

filename = "data.ics"
url = "http://wise-tt.com/wtt_um_feri/"
course = 'RIT UN'

def download():
    profile = webdriver.FirefoxProfile()

    profile.set_preference("browser.download.folderList", 2)
    profile.set_preference("browser.download.manager.showWhenStarting", False)
    profile.set_preference("browser.download.dir", os.getcwd())
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream, text/calendar,application/vnd.sus-calendar,text/x-vcalendar")

    options = Options()
    options.add_argument("--headless")

    browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
    
    browser.get("http://wise-tt.com/wtt_um_feri/")
    wait = WebDriverWait(browser, 4)
    
    print("Starting click for course.")
    element = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt85_label")))
    element.click()
    print("Clicked course menu.")


    print("\nStarting click for {}.".format(course))
    elementType = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt85_6")))
    elementType.click()
    print("Clicked {}.".format(course))

    time.sleep(5)
    print("\nStarting to download file")
    elementType = wait.until(EC.presence_of_element_located((By.ID, "form:j_idt151")))
    elementType.click()
    print("\nDownloaded file.")

    time.sleep(2)
    os.rename("calendar.ics", filename)

    return filename

if __name__ == "__main__":
    if( len(sys.argv) - 1 == 1 ):
        pass

    if download():
        print("Successfuly finished downloading.")
