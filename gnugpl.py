import nltk
from nltk.tokenize import *

class GPL:

    def __init__(self):
        self.filename = 'corpus/GPL3.txt'
        self.text = ''
        self.load()
    
    def removeNonAscii(self, s): 
        return "".join(i for i in s if ord(i)<128)
        
    def load(self):
        fd = open(self.filename, 'r')
        for line in fd.readlines():
            self.text += self.removeNonAscii(line.lower())
        fd.close
        
    def tokenz(self, alpha=True):
        tokz = wordpunct_tokenize(self.text)
        if alpha:
            tokz = [tok for tok in tokz if tok.isalpha()]
        return tokz
    
    def normalized_text(self):
        tokz = wordpunct_tokenize(self.text)
        return ' '.join(tokz)
        
    def Text(self):    
        return nltk.Text(self.tokenz())
    
    def __str__(self):
        return self.text
    
    def __getitem__(self, token):
        t = self.Text()
        return t.vocab()[token] 
               
    def top(self, n=20):
        t = self.Text()
        for word in t.vocab().keys()[0:n]:
            print word, t.vocab()[word]    
        
if __name__ == '__main__':  

    gpl = GPL()
    #print gpl.tokenz()
    gpl.top(50) 
    #print gpl.text
    #print gpl.normalized_text()   
    print gpl
    print gpl['the'] 