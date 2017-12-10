#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2017 urbikn <urbikn@knuples.net>
#
# Distributed under terms of the MIT license.

"""
    Downloads the data of the URL:  https://feri.um.si/urniki5/groups.php
"""

import requests
import datetime


# Predefined variables (! CHANGE ONLY WHEN REALLY NEEDED !)
now = datetime.datetime.now()
session = requests.session()
file_name = "test.html"

def download():
    # Data needed to get information from site
    url = "https://feri.um.si/urniki5/groups.php"
    current_datetime = "%d.%d.%d" % (now.day, now.month, now.year)
    params = {"branch_id":58,
              "branch_index":1,
              "branch_selector":1,
              "date_field": current_datetime,
              "branch_response": "{\"result\":[1,[{\"name\":\"RIT+UN+-+RAČUNALNIŠTVO+IN+INFORMACIJSKE+TEHNOLOGIJE+(BU20)\",\"code\":\"BU20\",\"branch_id\":\"58\",\"year\":\"1\"}],{\"\":+[]}]"
              }

    site = session.post(url, data=params)

    # returns website data as string
    data = str(site.content, "utf-8", errors="repeat")
    return data

