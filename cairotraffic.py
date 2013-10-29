import sys
import re
import nltk

class CairoTraffic:
    
    def __init__(self, filein='corpus/cairotraffic.txt', debug=True):
        self.filein = filein
        self.debug = debug
        self.data = []
        self.load()
        #print self.data
    
    def load(self):
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
        
    def show_traffic(self):
        for tweet in self.data:
            self.print_debug('\nTweet:\n')
            traffic = {
                'from': [],
                'to': []
            }
            for tagged_token in tweet['tokens']:
                self.print_debug('\tTagged token:' + str(tagged_token))
                if tagged_token[1] == 'FROM':
                   traffic['from'].append(tagged_token[0])
                elif tagged_token[1] == 'TO':
                   traffic['to'].append(tagged_token[0])
                else:
                    pass
            print ' '.join(traffic['from']), '=>', ' '.join(traffic['to']), ' STATUS:', tweet['sentiment']
            self.print_debug('\n')
        

if __name__ == '__main__':
    
    ct = CairoTraffic(debug=False)
    ct.show_traffic()