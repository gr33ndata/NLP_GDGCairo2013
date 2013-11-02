import sys
import json
import urllib2
import nltk

from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize
        
def fdist2csv(fdist, csv_file=''):
    fd = open(csv_file, 'w')
    fd.write('token,freq\n')
    for item in fdist:
        line = '%s,%d\n' % (item[0], item[1])
        fd.write(line)
    fd.close()
         
def removeNonAscii(s): 
        return "".join(i for i in s if ord(i)<128)

def wiki_fdist(topic='Egypt', max_tokenz=200):
    fdist = []
    url = 'http://en.wikipedia.org/w/index.php?title=%s&printable=yes' % (topic)
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0')]
    fd = opener.open(url)
    wiki_html = fd.read()
    wiki_text = nltk.clean_html(wiki_html)
    wiki_text = removeNonAscii(wiki_text)
    wiki_text = wiki_text.lower() 
    #print wiki_text[0:max_tokenz], '...\n'
    tokenz = word_tokenize(wiki_text)
    tokenz = [token.strip() for token in tokenz]
    tokenz = [token for token in tokenz if len(token) > 1]
    nltk_txt = nltk.Text(tokenz)
    for word in nltk_txt.vocab().keys()[0:100]:
        fdist.append([word, nltk_txt.vocab()[word]])
    return fdist
        
if __name__ == '__main__':

    topics = ['Egypt', 'Tunisia', 'Lebanon']
    
    for topic in topics:
        csv_file = '%s.csv' % topic
        fdist = wiki_fdist(topic, max_tokenz=1000)
        print topic, '=', str(fdist)
        fdist2csv(fdist, csv_file)