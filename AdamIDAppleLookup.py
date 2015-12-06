#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import AppleLookup
import time # I'll use this to slow down the number of queries to Apple
from datetime import datetime

# open an output file
with open('D:\\projects\\AppPicker\\app strength\\adamidlookup_out.csv', 'w', newline='',encoding='utf-8') as outfile:
    writer = csv.writer(outfile, delimiter=' ', quotechar='|', escapechar='~', doublequote=False, quoting=csv.QUOTE_NONNUMERIC)

    writer.writerow(['appID','Downloads','Developer','Title','Price','Current Rating',
                     'Current Rating Count','Rating','Rating Count','Screenshots','iPad Screenshots','Primary Genre',
                     'Genres','Supported Devices','Seller URL','Desc Length','Days Released'])

    # read from input file
    adamidfile = 'D:\\projects\\AppPicker\\app strength\\adamidgroup.csv'
    with open(adamidfile, newline='\n', encoding='utf-8') as csvfileh:
        #reader = csv.DictReader(csvfileh, fieldnames=('adam_id', 'counts','user_id'), delimiter=',',quoting=csv.QUOTE_NONE)
        reader = csv.DictReader(csvfileh, fieldnames=('adam_id', 'counts'), delimiter=',',quotechar='"')

        i = 1
        for row in reader:
            adamid = row['adam_id']

            downloadcount = row['counts']
            #userid = row['user_id']

            if adamid=='adam_id': continue
            #if i == 10: break

#            print('adamid: {}, count: {}'.format(adamid, downloadcount))

            result = AppleLookup.lookup(adamid)
            appjson = json.loads(result)
            
            if 'results' in appjson and len(appjson['results']) >= 1:
                if i % 10 == 0:
                    time.sleep(1)
                    print('Record: {}'.format(i))
                if i % 255 == 0: # throttle API calls a little
                    time.sleep(2)
                if i == 10000:
                    break

                appjson = appjson['results'][0]
                
                if 'kind' not in appjson:
                    if 'wrapperType' not in appjson:
                        adamtype = 'NA'
                    else:
                        adamtype = appjson['wrapperType']
                else:
                    adamtype = appjson['kind']
                
                if adamtype != 'software':
#                     writer.writerow([adamid,downloadcount,adamtype,'-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
                    print('Skipping adam_id {} because type = {}'.format(adamid, adamtype))
                    continue

                developer = appjson.get('artistName', 'NA')
                title = appjson.get('trackName', 'NA')
                price = appjson.get('price', 'NA')
                currRating = appjson.get('averageUserRatingForCurrentVersion', 0.0)
                currRatingCount = appjson.get('userRatingCountForCurrentVersion', 0.0)
                rating = appjson.get('averageUserRating', 0.0)
                ratingCount = appjson.get('userRatingCount', 0.0)
                
                nbrScreenshots = len(appjson.get('screenshotUrls',{}))
                nbriPadscreenshots = len(appjson.get('ipadScreenshotUrls',{}))
                primarygenre = appjson.get('primaryGenreName','NA')
                genres = ','.join(appjson.get('genres',{}))
                nbrSupportedDevices = len(appjson.get('supportedDevices',{}))
                sellerUrl = appjson.get('sellerUrl','NA')
                desclength = len(appjson.get('description',''))
                try:
                    daysreleased = (datetime.now() - datetime.strptime(appjson['releaseDate'],'%Y-%m-%dT%H:%M:%SZ')).days
                except:
                    daysreleased = 'NA'
                    
                writer.writerow([adamid,downloadcount,developer,title,price,currRating,currRatingCount,rating,ratingCount,
                                 nbrScreenshots,nbriPadscreenshots,primarygenre,genres,nbrSupportedDevices,sellerUrl,desclength,daysreleased])
                i += 1
            else:
#                 writer.writerow([adamid,downloadcount,'-','-','-','-','-','-','-','-','-','-','-','-','-','-','-'])
                print('No results for adam_id {}'.format(adamid))
outfile.close()