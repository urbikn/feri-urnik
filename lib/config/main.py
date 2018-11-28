#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 urbikn <urbikn@knuples>
#
# Distributed under terms of the MIT license.

"""
    The main script to change program/year/course in confg/user_data.json file
"""

import json

user_data_path = '../../config/user_data.json'
user_data_types = ['program','year','course'] # The way they're specified in the user_data.json


def changeWithData(data, type):
    '''
    Uses data to get list of available options and user decides which one to chose by inputing a number of the option

    args:
        data (List)                             - the list of options 
        type (int) (0:program,1:year,2:course ) - to specify configuration to change

    return:
        None
    '''
    
    options = [ data[i][1] for i in range(len(data)) ]
    print(user_data_types[type].capitalize(), "options to choose from:"  )
    for i in range(len(options)):
        print("   [{0}] {1}".format(i+1, options[i]))

    number = None
    while True:
        value = input("Number selected: ")
        # In case someone inputs something that isn't a number
        try:  number = int(value) - 1
        except ValueError: print("Wrong input inserted. I need a number..")
        break

    choice = options[number]
    with open(user_data_path, 'r+') as f:
        data = json.loads(f.read())
        data['info'][ user_data_types[type] ] = choice
        f.seek(0)
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.truncate()

    print("Updated", user_data_types[type].capitalize(),"\n")




def change(type, browser=None):
    '''
    Gets data from lib.downloader.downloader & lib.downloader.menu to get list of available options and user decides which one to chose by inputing a number of the option

    args:
        type (int) (0:program,1:year,2:course ) - to specify configuration to change

    return:
        None
    '''
    if not browser:
        import sys
        sys.path.append('../downloader')
        from downloader import Download

        # Creates a browser, loads website and gets list inside menu
        download = Download()
        download.setUp()

        browser = download.browser

    import menu

<<<<<<< HEAD
    # Creates a browser, loads website and gets list inside menu
    download = Download()
    download.setUp()
    data = menu.listItems(download.browser,type)

=======

    # websites generates by first clicking program, which generates year and clicking year generates courses ( and that's what I'm doing )
    if type > 0:
        f = open(user_data_path,'r')
        data = json.loads(f.read())['info']
        b = 0
        while b != type:
            menu.clickItem(browser,b,data[user_data_types[b]])
            b+=1


    data = menu.listItems(browser,type)
>>>>>>> e6c6d92... Add instance of browser as paramater in configuration script
    # Changes configuration inside user_json
    changeWithData(data,type)

    download.stop()
