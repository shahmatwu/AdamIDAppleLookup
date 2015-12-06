#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib.request
import sys

LookupURL = 'https://itunes.apple.com/lookup?id='

def lookup(appid):
    url = LookupURL+str(appid)
    try:
        response = urllib.request.urlopen(url)
        result = response.read().decode('utf-8')
    except:
        print('Unexpected error: {}. Adam_id: {}'.format(sys.exc_info()[0], appid))
        return '{"resultCount":1}'
    return result