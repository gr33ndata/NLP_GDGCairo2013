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
        with open(self.filein,'r') as fdin:
            for line in fdin.readlines():
                tagged_tokenz = []
                tokenz = re.split('\s+', line)
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
        

def demo1():
    
    ct = CairoTraffic(filein='corpus/democairotraffic.txt', debug=False)
    ct.show_traffic()
    
    print 'Unigram tagger:'
    ct.unigram_tag('Suez to Ismailia za7ma')
    ct.unigram_tag('Ismailia to Suez za7ma')
    
    print 'Bigram tagger:'
    ct.bigram_tag('Ismailia to Suez za7ma', backoff=True)
    ct.bigram_tag('Suez to Ismailia za7ma', backoff=True)
    ct.bigram_tag('Alex to October za7ma', backoff=True)

def demo2():

    ct = CairoTraffic(filein='corpus/cairotraffic.txt', debug=False)
    
    
if __name__ == '__main__':
    
    demo1()
    
