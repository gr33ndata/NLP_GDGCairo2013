import sys
import re
import nltk

class CairoTraffic:
    
    def __init__(self, filein='', debug=True):
        self.filein = filein
        self.debug = debug
        self.data = []
        self.load()
        #print self.data
    
    def load(self):
        ''' Loads tweet fromm filein
            Then converts it into the following structure
                tokens: [], sentiment: za7ma
            @tokens: a listt of tuples, (word, pos)
            @sentiment: za7ma foll etc        
        '''
        fdin = open(self.filein,'r')
        for line in fdin.readlines():
            tagged_tokenz = []
            tokenz = re.split('\s+', line)
            tokenz = [token.strip() for token in tokenz if len(token.strip()) > 1]
            for token in tokenz:
                if token.find('/') == -1:
                    tagged_tokenz.append((token, 'NN'))
                else:
                    token_txt, token_tag = token.split('/')
                    tagged_tokenz.append((token_txt, token_tag))
            self.data.append({
                'tokens': tagged_tokenz, 
                'sentiment': 'zeft'
            })
        fdin.close()
        
    def print_debug(self, message):
        if self.debug:
            print message
    
    def unigram_tag(self, text):
        ''' Unigram Tagger are based on a simple statistical algorithm, 
            For each token, assign the tag that is most likely for that token.
            It only works for tokens already seen in training set. 
        '''
        trainingset = []
        for tweet in self.data:
            trainingset.append(tweet['tokens'])
        unigram_tagger = nltk.UnigramTagger(trainingset)
        tokenz = re.split('\s+', text)
        pos = unigram_tagger.tag(tokenz)
        print pos
        return pos
        
    def bigram_tag(self, text, backoff=True):
        ''' Bigram Tagger cosider previous word too, 
            As soon as it encounters a new word,
            the tagger fails to tag the rest of the sentence.
            Backoff, uses unigram taggers when bigram fails.
            Still, problem with unseen tokens.
        '''
        trainingset = []
        for tweet in self.data:
            trainingset.append(tweet['tokens'])
        if backoff:
            default_tagger = nltk.DefaultTagger('NN')
            unigram_tagger = nltk.UnigramTagger(trainingset, backoff=default_tagger)
            bigram_tagger = nltk.BigramTagger(trainingset, backoff=unigram_tagger)
        else:
            bigram_tagger = nltk.BigramTagger(trainingset)
        tokenz = re.split('\s+', text)
        pos = bigram_tagger.tag(tokenz)
        print pos
        return pos
    
    def pos_featrues(self, tweet):
        ''' Helper function for ml_tag()
        '''
        tweet_featurs = []
        #print 'Tokz::', str(tweet)
        for i in range(len(tweet['tokens'])):
            featurs = {}
            featurs['word'] = tweet['tokens'][i][0].strip('#').lower()
            featurs['hashtag'] = tweet['tokens'][i][0].startswith('#')
            featurs['caps'] = tweet['tokens'][i][0][0].isupper()
            try:
                featurs['prev'] = tweet['tokens'][i-1][0].lower()
            except:
                featurs['prev'] = ''
            try:
                featurs['next'] = tweet['tokens'][i+1][0].lower()
            except:
                featurs['next'] = ''
            tweet_featurs.append((featurs, tweet['tokens'][i][1]))
        return tweet_featurs
        
    def ml_tag(self, text, backoff=True):
        ''' Machine Learning Tagger cosider featureset, 
            As soon as it encounters a new word,
            the tagger fails to tag the rest of the sentence.
            Backoff, uses unigram taggers when bigram fails.
            Still, problem with unseen tokens.
        '''
        trainingset = []
        for tweet in self.data:
            trainingset = trainingset + self.pos_featrues(tweet)
        #classifier = nltk.DecisionTreeClassifier.train(trainingset)    
        classifier = nltk.NaiveBayesClassifier.train(trainingset)    
        tokenz = re.split('\s+', text)
        tokenz = [(token,'') for token in tokenz]
        tokenz_features = self.pos_featrues({'tokens': tokenz})
        tagged_text = []
        for token in tokenz_features:
            tag = classifier.classify(token[0])
            tagged_text.append((token[0]['word'], tag))
        print tagged_text
        return tagged_text
        
    def parse_tweet(self, tweet):
        ''' Returns the following structure
            from: [],to: [],sentiment: tweet[sentiment]
        '''
        traffic_tweet = {
            'from': [],
            'to': [],
            'sentiment': tweet['sentiment']
        }
        for tagged_token in tweet['tokens']:
            self.print_debug('\tTagged token:' + str(tagged_token))
            if tagged_token[1] == 'FROM':
                traffic_tweet['from'].append(tagged_token[0])
            elif tagged_token[1] == 'TO':
                traffic_tweet['to'].append(tagged_token[0])
            else:
                pass
        return traffic_tweet
            
    def show_traffic(self):
        ''' Displays the loaded file in the form of From => To and Status
        '''
        for tweet in self.data:
            self.print_debug('\nTweet:\n')
            traffic_tweet = self.parse_tweet(tweet)
            print ' '.join(traffic_tweet['from']), '=>', ' '.join(traffic_tweet['to']), ' STATUS:', traffic_tweet['sentiment']
            self.print_debug('\n')
        

def demo0():

    ct = CairoTraffic(filein='corpus/democairotraffic.txt', debug=False)
    
    print '\nTagged Tweets'
    ct.show_traffic()

def demo1():
    
    ct = CairoTraffic(filein='corpus/democairotraffic.txt', debug=False)
    #ct.show_traffic()
    
    print '\nUnigram tagger:'
    ct.unigram_tag('Suez to Ismailia za7ma')
    ct.unigram_tag('Ismailia to Suez za7ma')
    
       
def demo2():
    
    ct = CairoTraffic(filein='corpus/democairotraffic.txt', debug=False)
    #ct.show_traffic()    
    
    print '\nBigram tagger:'
    ct.bigram_tag('Suez to Ismailia za7ma', backoff=True)
    ct.bigram_tag('Ismailia to Suez za7ma', backoff=True)
    ct.bigram_tag('Cairo to October za7ma', backoff=True)
    ct.bigram_tag('Alex towards Cairo za7ma', backoff=True) 

def demo3():
    
    #ct = CairoTraffic(filein='corpus/democairotraffic.txt', debug=False)
    ct = CairoTraffic(filein='corpus/cairotraffic.txt', debug=False)
    #ct.show_traffic()    
    
    print '\nNaive Bayes tagger:'
    ct.ml_tag('Suez to Ismailia za7ma')
    ct.ml_tag('Ismailia to Suez za7ma')
    ct.ml_tag('Cairo to October za7ma')
    ct.ml_tag('Traffic from alex towards cairo za7ma') 
    ct.ml_tag('October bridge za7ma fashkh from Zamalek towards Down Town in the direction of Tahrir')        


def demo4():

    ct = CairoTraffic(filein='corpus/cairotraffic.txt', debug=False)
    
    
if __name__ == '__main__':
    
    demo0()
    demo1()
    demo2()
    demo3()
    
