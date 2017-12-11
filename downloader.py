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
import requests

# Predefined variables (! CHANGE ONLY WHEN REALLY NEEDED !)
phantomjs_path = "lib/PhantomJS/bin/phantomjs"
url = "https://feri.um.si/urniki5/groups.php"
program = "RAČUNALNIŠTVO IN INFORMACIJSKE TEHNOLOGIJE (BU20)"
letnik = "1"

params = {
	"date_field":"11.12.2017",
	"iCal_data":"group_week",
	"pagename":"groups",
	"year_index":"1",
	"year_response":"3",
	"branch_id":"58",
	"branch_index":"1"
}

headers = {"User-Agent":"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:57.0) Gecko/20100101 Firefox/57.0"}

def download():
    s = requests.Session()
    s.headers.update(headers)

    r = s.post("https://feri.um.si/urniki5/lib/iCal.php?r=group_ical&type=group_week", data=params)

    return(r.content)
