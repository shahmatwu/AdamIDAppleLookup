#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request

LookupURL = 'https://itunes.apple.com/lookup?id='

def lookup(appid):
    url = LookupURL+str(appid)
    response = urllib.request.urlopen(url)
    result = response.read().decode('utf-8')
    return result