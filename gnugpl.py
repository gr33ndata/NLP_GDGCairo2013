import nltk
from nltk.tokenize import *

class GPL:

    def __init__(self):
        ''' Loads the text of the GPL License
            And put it into self.text
        '''
        self.filename = 'corpus/GPL3.txt'
        self.text = ''
        self.load()
    
    def removeNonAscii(self, s): 
        return "".join(i for i in s if ord(i)<128)
        
    def load(self):
        ''' Loads data from file.
        '''
        fd = open(self.filename, 'r')
        for line in fd.readlines():
            self.text += self.removeNonAscii(line.lower())
        fd.close
        
    def tokenz(self, alpha=True):
        ''' Tokenize the loaded text,
            Then remove non-alphanumeric tokens.
        '''
        tokz = wordpunct_tokenize(self.text)
        if alpha:
            tokz = [tok for tok in tokz if tok.isalpha()]
        return tokz
    
    def normalized_text(self):
        tokz = wordpunct_tokenize(self.text)
        return ' '.join(tokz)
        
    def Text(self):    
        ''' Puts our text into the nltk.Text() object.
        '''
        return nltk.Text(self.tokenz())
    
    def __str__(self):
        ''' Returns the text readed from file.
        '''
        return self.text
    
    def __getitem__(self, token):
        ''' Returns the count of token appears in our document.
        '''
        t = self.Text()
        return t.vocab()[token] 
               
    def top(self, n=20):
        ''' Returns the top n tokens along with their counts.
        '''
        t = self.Text()
        for word, count in t.vocab().items()[0:n]:
            print word, count    
        
if __name__ == '__main__':  

    gpl = GPL()
    print gpl.tokenz()
    gpl.top(50) 
    print gpl.text
    print gpl.normalized_text()   
    print gpl
    print gpl['the'] 