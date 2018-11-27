#! /usr/bin/env python3
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

types = ['program','year','course']
wait = None
tagID = None

def __reconfigure__(browser,type):
    '''
    Reconfigures specified type settings in user configuration

    args:
        browser (webdriver.Firefox)             - object to use the browser,
        type (int) (0:program,1:year,2:course ) - to specify which dropdown menu to use

    return:
        None
    '''
    data = listItems(browser,type)

    import sys
    sys.path.append("../config")
    import main
    main.change(data,type)


def findMenu( browser, type ):
    '''
    Finds the menu and clicks it ( so it can generate data ).

    args:
        browser (webdriver.Firefox)             - object to use the browser,
        type (int) (0:program,1:year,2:course ) - to specify which dropdown menu to use

    return:
        string                                  - ID of the menu

        ( For now the website works by using the ID and adding string to represent something
          like for example ID_label, ID_items, etc.  )
    '''
    
    wait = webdriver.support.ui.WebDriverWait(browser,4)

    # Finds the ID of the dropdown menu in the DOM
    script ="return $('.noBorderBasicTable:eq(1) label:eq({})').get()[0].id.match(/\d+/)[0]".format(type)
    tagID = "form:j_idt" + browser.execute_script(script)
    element = wait.until(EC.presence_of_element_located((By.ID, tagID + "_label")))
    element.click()
 
    return tagID



def listItems( browser, type ):
    '''
    list all items inside the menu.

    args:
        browser (webdriver.Firefox)             - object to use the browser,
        type (int) (0:program,1:year,2:course ) - to specify which dropdown menu to use

    return:
        List( string,string )                   - ID of element and value
    '''

    tagID = findMenu(browser, type)
    time.sleep(2)

    # Scripts gets all items inside menu
    script = "return (()=>{{return $('#{}').children()}})().toArray()".format(tagID.replace(':','\\\\:')+"_items")

    values = browser.execute_script(script)
    output = []
    for data in values :
        if( data.text.strip() ): # text isn't empty
            output.append( ( data.get_attribute('id') , data.text) )

    return output




def clickitem( browser, type, data ):
    '''
    Clicks an item inside the dropdown menu.

    args:
        browser (webdriver.Firefox)             - object to use the browser,
        type (int) (0:program,1:year,2:course ) - to specify which dropdown menu to use
        data (string)                           - the value of the dropdown item to click
    
    return:
        None
    '''
    tagID = findMenu( browser, type )
    time.sleep(2)

    # Finds and clicks the specific item using data as a value by which to search
    script = """return $(document.getElementById('{0}')).find("li[data-label='{1}']")[0].id""".format(tagID+'_items',data)
    try:
        ID = browser.execute_script(script)
        elementType = wait.until(EC.presence_of_element_located((By.ID, ID )))
        elementType.click()
    except:
        print("Couldn't find",types[type], data)
        print("Need to reconfigure settings")
        __reconfigure__(browser,type)




if __name__ == '__main__':
    pass
