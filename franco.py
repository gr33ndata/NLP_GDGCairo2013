import sys
import nltk
from nltk.tokenize import word_tokenize, wordpunct_tokenize, sent_tokenize

from sklearn.feature_extraction import DictVectorizer
from sklearn.naive_bayes import GaussianNB, MultinomialNB

text = {}

''' Load data from arabizi.txt
    Then put data as key & value in text
'''
def load(filename='corpus/franco.txt'):
    fd = open(filename)
    for line in fd.readlines():
        try:
            key, val = line.split(':', 1)
            text[key] = val.lower().strip()
        except:
            pass


''' Displays data loaded from arabizi.txt
    Data is put as key & value pairs in text
'''
def show():
    for key in text:
        print key + ':' + text[key][0:100] + '... (Length: ' + str(len(text[key])) + ' characters)'
        words = wordpunct_tokenize(text[key])
        print key + ':' + ','.join(words[0:100]) + '... (Length: ' + str(len(words)) + ' words)'
    print '\n'

''' Get tokenz freuquencies
    mood: char, 2-gram, word
'''
def get_freq(mode='char'):
    fdist = {}
    for label in text:
        fdist[label] = []
        if mode == 'char':
            tokenz = [char for char in text[label]]
        if mode.endswith('gram'):
            n = int(mode.split('-')[0])
            tokenz = [text[label][i:i+n] for i in range(len(text[label]))]
        else:
            tokenz = word_tokenize(text[label])   
        nltk_txt = nltk.Text(tokenz)
        #nltk_txt.plot()
        for char in nltk_txt.vocab().keys():
            fdist[label].append((char, nltk_txt.vocab()[char]))
        fdist[label].sort()
    return fdist 
        
def print_debug(message, debug=False):
    if debug:
        print message
            
''' Classify English vs Arabizi
'''
def classifier(n=1):
    v = DictVectorizer(sparse=False)
    featureset = []
    labels = []
    for label in text:
        tokenz = [text[label][i:i+n] for i in range(len(text[label]))]
        fdist = nltk.FreqDist(tokenz)
        features = {}
        for tok in fdist.keys():
            features[tok] = fdist[tok]
        print label, features
        featureset.append(features)
        labels.append(label)
    featureset_scikit = v.fit_transform(featureset)
    nb = MultinomialNB(alpha=0.1, fit_prior=False)
    nb.fit(featureset_scikit, labels)
    return {'learner': nb, 'vectorizer': v, 'n': n}

''' Convert string to featureset
    Then use scikit-learn and classifier to classify it.
'''
def predict(text='', classifier=None):
    n = classifier['n']
    v = classifier['vectorizer']
    nb = classifier['learner']
    tokenz = [text[i:i+n] for i in range(len(text))]
    fdist = nltk.FreqDist(tokenz)
    features = {}
    for tok in fdist.keys():
        features[tok] = fdist[tok]
    featureset_scikit = v.transform(features)
    y = nb.predict(featureset_scikit)
    print 'Class:', y[0]
    
    

#import nltk
#import arabizi
#c = arabizi.classifier(n=2)
#arabizi.predict('naharak zay el 3asal', c)

                
load() 
#show()   



if __name__ == '__main__':

    DEBUG = False
    
    for key in text:
        msg =  key + ' => Length: ' + str(len(text[key]))
        print_debug(msg, debug=DEBUG)
    print ''
    
    for key in text:
        lex_richness = float( len(text[key])) / len(set(text[key]) )
        msg = key + ' => Lexical richness: ' + str(lex_richness)
        print_debug(msg, debug=DEBUG)
    print_debug('', debug=DEBUG)
    
    fdist = get_freq(mode='1-gram')
    for label in text:
        print label, fdist[label]
    
    try:
        input_text = ' '.join(sys.argv[1:])
        print 'Text:', input_text
        c = classifier(n=2)
        predict(input_text, c)
    except:
        print 'Please type some text'
        pass
        
    
        