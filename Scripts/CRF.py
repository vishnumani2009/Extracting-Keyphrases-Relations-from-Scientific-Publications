from itertools import chain

import nltk
import sklearn
import scipy.stats
from sklearn.metrics import make_scorer
from sklearn.cross_validation import cross_val_score
from sklearn.grid_search import RandomizedSearchCV

import sklearn_crfsuite
from sklearn_crfsuite import scorers
from sklearn_crfsuite import metrics
from sklearn.cross_validation import train_test_split

def word2features(sent, i):
    #print sent
    word = sent[i][0]
    postag = sent[i][1]
   
    features = {
        'bias': 1.0,
        'word[-3:]': word[-3:],
        'word[-2:]': word[-2:],
        'postag': postag,
        'postag[:2]': postag[:2],
    }
    if i > 0:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        features.update({
            '-1:postag': postag1,
            '-1:postag[:2]': postag1[:2],
        })
    else:
        features['BOS'] = True

    if i < len(sent) - 1:
        word1 = sent[i + 1][0]
        postag1 = sent[i + 1][1]
        features.update({
            '+1:postag': postag1,
            '+1:postag[:2]': postag1[:2],
        })
    else:
        features['EOS'] = True
    #print features
    return features


def sent2features(sent):
    tempsent=[]
    sent=sent.split()
    for i in range(len(sent)):
        word=sent[i].split("|")[0]
        postag=nltk.pos_tag([word])[0][1]
	#print postag
        label=sent[i].split("|")[1]
        tempsent.append((word,postag,label))
    return [word2features(tempsent, i) for i in range(len(tempsent))]

def sent2labels(sent):
    tempsent=[]
    sent=sent.split()
    for i in range(len(sent)):
        word=sent[i].split("|")[0]
        postag=nltk.pos_tag([word])[0][1]
        label=sent[i].split("|")[1]
        tempsent.append((word,postag,label))
    return [label for token, postag, label in tempsent]

def sent2tokens(sent):
    tempsent=[]
    sent=sent.split()
    for i in range(len(sent)):
        word=sent[i].split("|")[0]
        postag=nltk.pos_tag([word])[0][1]
        label=sent[i].split("|")[1]
        tempsent.append((word,postag,label))
    return [token for token, postag, label in tempsent]


def createdata():
    fread=open("dev_corpus.txt","r")
    lines=fread.readlines()
    train_sents,test_sents = train_test_split(lines,test_size=0.33,random_state=50)

    X_train = [sent2features(s) for s in train_sents]
    y_train = [sent2labels(s) for s in train_sents]

    X_test = [sent2features(s) for s in test_sents]
    y_test = [sent2labels(s) for s in test_sents]

    #print sent2features(train_sents[0])[0]



    crf = sklearn_crfsuite.CRF(
        algorithm='lbfgs',
        c1=0.1,
        c2=0.1,
        max_iterations=100,
        all_possible_transitions=True
    )
    print "training"
    crf.fit(X_train, y_train)

    labels = list(crf.classes_)
    labels.remove('O')
    print labels
    y_pred = crf.predict(X_test)
    print y_pred
    metrics.flat_f1_score(y_test, y_pred,average='weighted', labels=labels)

createdata()
