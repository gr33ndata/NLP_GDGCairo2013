import sys
import json
import urllib

import nltk
from nltk import clean_html

from feedparser import _parse_date as parse_date

try:
    from googlekey import key as apikey
except:
    print '''Befor starting, you need to create a new file, googlekey.py \nThen write in it key=[your Google API key]'''
    sys.exit() 
    
#print apikey

class GooglePlus:

    def __init__(self, userId='+nilefm'):
        self.userId = userId
    
    def enum_weekdays(self, dayId):
        weekdays = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        if dayId > 6:
            return weekdays[0]
        else:
            return weekdays[dayId]
                
    def parse_rfc3339_date(self, dateString):
        mydt = parse_date(dateString.replace('Z','-02:00'))
        weekdayId = mydt.tm_wday
        hour = mydt.tm_hour
        if hour >= 8 and hour <= 17:
            time_of_day = 'Morning'
        elif hour > 17 and hour < 22:
            time_of_day = 'Evening'
        else:
            time_of_day = 'Night'    
        retobj = {
            'weekdayId': weekdayId,
            'weekdayName': self.enum_weekdays(weekdayId),
            'hour': hour,
            'time_of_day': time_of_day,
        } 
        return retobj
    
    def removeNonAscii(self, s): 
        return "".join(i for i in s if ord(i)<128)
          
    def get_public_feed(self, out_file='', max_pages=1):
        if max_pages == 0:
            return []
        ret_data = []
        url = 'https://www.googleapis.com/plus/v1/people/%s/activities/public?key=%s&maxResults=100' % (self.userId, apikey)
        fd = urllib.urlopen(url)
        json_data = fd.read()
        data = json.loads(json_data)
        #print 'Fetched activities:', len(data['items'])
        nextPageToken = data['nextPageToken']
        for item in data['items']:
            title = item['title']
            content = self.removeNonAscii(clean_html(item['object']['content'])).lower()
            time = self.parse_rfc3339_date(item['published']) 
            plusoners = item['object']['plusoners']['totalItems']
            #print content, str(time)
            #print str(plusoners), str(time)
            ret_data.append({
                'title': title,
                'content': content,
                'time': time,    
                'plusoners': plusoners,
            })
            
        ret_data = ret_data + self.get_public_feed(out_file='', max_pages=max_pages-1)     
        
        if out_file == '':
            return ret_data
        else:
            print 'Fetched activities:', len(ret_data)
            with open(out_file, 'w') as fd_out:
                for data_item in ret_data:
                    #print data_item['plusoners']
                    line = '%s, %s, %s, %s\n' % (str(data_item['plusoners']), str(data_item['time']['hour']), str(data_item['time']['weekdayName']), str(data_item['content']))
                    fd_out.write(line)
            print 'Activities written to', out_file

            
if __name__ == '__main__':

    gplus = GooglePlus(userId='+nilefm')
    #print gplus.parse_rfc3339_date('1937-01-01T03:00:27.87+02:00')
    gplus.get_public_feed(out_file='corpus/nilefm.csv', max_pages=20)