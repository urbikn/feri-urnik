#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    Downloads the data of the URL:  https://feri.um.si/urniki5/groups.php.

    The website uses AJAX so we need to get the javascript data and fill out the form.
"""

from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time

# Predefined variables (! CHANGE ONLY WHEN REALLY NEEDED !)
phantomjs_path = "lib/PhantomJS/bin/phantomjs"
url = "https://feri.um.si/urniki5/groups.php"
program = "RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE (BU20)"
letnik = "1"

def download():
    # Data needed to get information from site
    driver = webdriver.PhantomJS(phantomjs_path)
    driver.get(url)
    
    # Gets input values to add values
    programInput = Select(driver.find_element_by_id("program"))
    letnikInput = Select(driver.find_element_by_id("year"))
    
    # Sets values of input and sleeps for a few seconds so new data can be shown on site
    programInput.select_by_visible_text(program)
    time.sleep(1)
    letnikInput.select_by_visible_text(letnik)
    time.sleep(3)
    
    inputTedenskiUrnik = driver.find_element_by_xpath("//input[@value='Prikaži tedenski urnik']")
    inputTedenskiUrnik.click()

    return driver.page_source

