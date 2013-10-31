import sys

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
        self.get_public_feed()
    
    def enum_weekdays(self, dayId):
        weekdays = ['Mon', 'Tues', 'Wed', 'Thur', 'Fri', 'Sat', 'Sun']
        if dayId > 6:
            return weekdays[0]
        else:
            return weekdays[dayId]
                
    def parse_rfc3339_date(self, dateString):
        mydt = parse_date(dateString)
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
          
    def get_public_feed(self):
        url = 'https://www.googleapis.com/plus/v1/people/%s/activities/public?key=%s' % (self.userId, apikey)
        print url
        #d = feedparser.parse(url)
        #for item in d.items:
        #    print item.title
            
if __name__ == '__main__':

    gplus = GooglePlus(userId='+nilefm')
    print gplus.parse_rfc3339_date('1937-01-01T03:00:27.87+02:00')