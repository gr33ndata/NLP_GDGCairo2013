import nltk
from nltk.tokenize import *

class GPL:

    def __init__(self):
        self.text = ''
        self.load()
    
    def removeNonAscii(self, s): 
        return "".join(i for i in s if ord(i)<128)
        
    def load(self, filename='corpus/GPL3.txt'):
        fd = open(filename, 'r')
        for line in fd.readlines():
            self.text += self.removeNonAscii(line.lower())
        fd.close
        
    def tokenz(self, alpha=True):
        tokz = wordpunct_tokenize(self.text)
        if alpha:
            tokz = [tok for tok in tokz if tok.isalpha()]
        return tokz
    
    def Text(self):    
        return nltk.Text(self.tokenz())
        
    def top(self, n=20):
        t = self.Text()
        for word in t.vocab().keys()[0:n]:
            print word, t.vocab()[word]    
        
if __name__ == '__main__':  

    gpl = GPL()
    #print gpl.tokenz()
    gpl.top(50)      