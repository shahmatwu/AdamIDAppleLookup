#!/usr/bin/env python
# -*- coding: utf-8 -*-

import csv
import json
import AppleLookup

# open an output file
with open('D:\\projects\\AppPicker\\app strength\\adamidlookup_out.csv', 'w', newline='',encoding='utf-8') as outfile:
    writer = csv.writer(outfile, delimiter='|', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    writer.writerow(['appID','Downloads','appPickerUserID','appleID','Developer','Title','Price','Current Rating','Current Rating Count','Rating','Rating Count'])

    # read from input file
    adamidfile = 'D:\\projects\\AppPicker\\app strength\\adamidgroup.csv'
    with open(adamidfile, newline='\n', encoding='utf-8') as csvfileh:
        reader = csv.DictReader(csvfileh, fieldnames=('adam_id', 'counts','user_id'), delimiter=',',quoting=csv.QUOTE_NONE)

        i = 0
        for row in reader:
            adamid = row['adam_id']

            downloadcount = row['counts']
            userid = row['user_id']

            if adamid=='adam_id': continue
            i += 1
            #if i == 10: break

            print('Record: {}'.format(i))
#            print('adamid: {}, count: {}'.format(adamid, downloadcount))

            result = AppleLookup.lookup(adamid)
            appjson = json.loads(result)
            
            if 'results' in appjson and len(appjson['results']) >= 1:
                devid = appjson['results'][0]['artistId']
                developer = appjson['results'][0]['artistName']
                title = appjson['results'][0]['trackName']
                price = appjson['results'][0]['price']

                if 'averageUserRatingForCurrentVersion' in appjson['results'][0]:
                    currRating = appjson['results'][0]['averageUserRatingForCurrentVersion']
                else:
                    currRating = 0.0

                if 'userRatingCountForCurrentVersion' in appjson['results'][0]:
                    currRatingCount = appjson['results'][0]['userRatingCountForCurrentVersion']
                else:
                    currRatingCount = 0.0

                if 'averageUserRating' in appjson['results'][0]:
                    rating = appjson['results'][0]['averageUserRating']
                else:
                    rating = 0.0

                if 'userRatingCount' in appjson['results'][0]:
                    ratingCount = appjson['results'][0]['userRatingCount']
                else:
                    ratingCount = 0.0

                writer.writerow([adamid,downloadcount,userid,devid,developer,title,price,currRating,currRatingCount,rating,ratingCount])
            else:
                writer.writerow([adamid,downloadcount,userid,'-','-','-','-','-','-','-','-'])
outfile.close()