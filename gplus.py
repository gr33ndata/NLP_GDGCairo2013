import sys
import json
import urllib

import nltk
from nltk import clean_html

from feedparser import _parse_date as parse_date
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

try:
    from googlekey import key as apikey
except:
    print '''Befor starting, you need to create a new file, googlekey.py \nThen write in it key=[your Google API key]'''
    sys.exit() 
    
#print apikey

class GooglePlus:

    def __init__(self, userId='+nilefm'):
        self.userId = userId
        self.data = []
    
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
        print 'Retrieving %s feed, %d pages left.' % (self.userId, max_pages)
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
            self.data = ret_data
            return ret_data

    def is_valid_token(self, token):
        if token.isalpha():
            return True
        elif token.startswith('#') and token[1:].isalpha():
            return True
            
    def analyze(self, plusoners_threshold=3, out_file=''):
        ''' Analyses the Google+ of userId
            Generates words collocations
            And top N tokens, wrt their frequencies.
            @plusoners_threshold: First of all, we split updats
                Those below certain plusone threshold,
                and those above or equals to it
            @out_file: if given, output will be printed to it
                Otherwise, it will be printed on screen
        '''
        text = {
            'above threshold': {'text': '', 'n': 0, 'd3': []}, 
            'below threshold': {'text': '', 'n': 0, 'd3': []} 
        }
        for item in self.data:
            if int(item['plusoners']) < 3:
                text['below threshold']['text'] += item['content']
                text['below threshold']['n'] += 1
            else:
                text['above threshold']['text'] += item['content']
                text['above threshold']['n'] += 1
        
        if out_file:
            fd = open(out_file, 'w')   
            STDOUT  = sys.stdout
            sys.stdout = fd     
            
        for label in text:
            print '\n', label.title()
            print 'Loaded updates:', text[label]['n']
            tokenz = wordpunct_tokenize(text[label]['text'])
            tokenz = [token for token in tokenz if self.is_valid_token(token)]
            txt = nltk.Text(tokenz)
            print 'Top 10 collecated tokens:' 
            txt.collocations(num=10, window_size=2)
            print 'Top 50 tokens:'
            for word in txt.vocab().keys()[0:50]:
                print word, ':', txt.vocab()[word]
                text[label]['d3'].append(["\"" + word + "\"", txt.vocab()[word]])
            print '\n'
            
        if out_file:
            fd.close()  
            sys.stdout = STDOUT  
            
        for label in text:
            print label
            print text[label]['d3']
                       
        # Returns text so we can play with it.
        return text
            
if __name__ == '__main__':

    gplus_Id = '+GDGCairoOrg'
    gplus = GooglePlus(userId=gplus_Id)
    #print gplus.parse_rfc3339_date('1937-01-01T03:00:27.87+02:00')
    out_file = 'corpus/%s.csv' % gplus_Id[1:]
    gplus.get_public_feed(out_file=out_file, max_pages=20)
    out_file = 'corpus/%s_analysis.txt' % gplus_Id[1:]
    gplus.analyze(out_file=out_file, plusoners_threshold=3)
    