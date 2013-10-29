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
        #print label, features
        featureset.append(features)
        labels.append(label)
    featureset_scikit = v.fit_transform(featureset)
    nb = MultinomialNB(alpha=0.1, fit_prior=False)
    nb.fit(featureset_scikit, labels)
    return {'learner': nb, 'vectorizer': v, 'n': n}

''' Convert string to featureset
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
    print y
    
    
'''
import nltk
import arabizi
c = arabizi.classifier(n=2)
arabizi.predict('naharak zay el 3asal', c)

'''
                
load() 
#show()   



if __name__ == '__main__':

    for key in text:
        print key, ' => Length: ', str(len(text[key]))
    print ''
    
    for key in text:
        print key , ' => Lexical richness: ',float(len(text[key])) / len(set(text[key]))
    print ''
    
    try:
        input_text = ' '.join(sys.argv[1:])
        print input_text
        c = classifier(n=2)
        predict(input_text, c)
    except:
        print 'Please type some text'
        pass
    
        