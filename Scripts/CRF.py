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
from collections import Counter

def print_state_features(state_features):
    for (attr, label), weight in state_features:
        print("%0.6f %-8s %s" % (weight, label, attr))


def word2features(sent, i):
    #print sent
    word = sent[i][0]
    postag = sent[i][1]
   
    features = {
        'bias': 1.0,
        'suffix': word[-3:],
        'postag': postag,
        'word':word,
    }

    if i==0:
	features['BOS']=True
    if i==len(sent)-1:
	features['EOS']=True


    if i ==1:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
	word2 = sent[i + 1][0]
        postag2 = sent[i + 1][1]
        features.update({
            '-1:postag': postag1,
            '-1:word': word1,
	    '-1:suffix': word1[-3:],
	   
            '+1:postag': postag2,
            '+1:word': word2,
	    '+1:suffix': word2[-3:],
        })

    if i==len(sent)-2:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
	word2 = sent[i + 1][0]
        postag2 = sent[i + 1][1]
        features.update({
            '-1:postag': postag1,
            '-1:word': word1,
	    '-1:suffix': word1[-4:],
	   
            '+1:postag': postag2,
            '+1:word': word2,
	    '+1:suffix': word2[-4:],
        })


#if pos ==2
    if i ==2:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
	word2 = sent[i - 2][0]
        postag2 = sent[i - 2][1]
	word3 = sent[i + 1][0]
        postag3 = sent[i + 1][1]
	word4 = sent[i + 2][0]
        postag4 = sent[i + 2][1]
        features.update({
            '-1:postag': postag1,
            '-1:word': word1,
	    '-1:suffix': word1[-3:],
	   
            '-2:postag': postag2,
            '-2:word': word2,
	    '-2:suffix': word2[-3:],

	    '+1:postag': postag3,
            '+1:word': word3,
	    '+1:suffix': word3[-3:],
	   
            '+2:postag': postag4,
            '+2:word': word4,
	    '+2:suffix': word4[-3:],
        })


    if i ==len(sent)-3:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
	word2 = sent[i - 2][0]
        postag2 = sent[i - 2][1]
	word3 = sent[i + 1][0]
        postag3 = sent[i + 1][1]
	word4 = sent[i + 2][0]
        postag4 = sent[i + 2][1]
        features.update({
            '-1:postag': postag1,
            '-1:word': word1,
	    '-1:suffix': word1[-3:],
	   
            '-2:postag': postag2,
            '-2:word': word2,
	    '-2:suffix': word2[-3:],

	    '+1:postag': postag3,
            '+1:word': word3,
	    '+1:suffix': word3[-3:],
	   
            '+2:postag': postag4,
            '+2:word': word4,
	    '+2:suffix': word4[-3:],
        })

    #print i,len(sent)
    if i >=3 and i<len(sent) - 3:
        word1 = sent[i - 1][0]
        postag1 = sent[i - 1][1]
        word2 = sent[i - 2][0]
        postag2 = sent[i - 2][1]
        word3 = sent[i - 3][0]
        postag3 = sent[i - 3][1]
	word4 = sent[i + 1][0]

        postag4 = sent[i + 1][1]
        word5 = sent[i + 2][0]
        postag5 = sent[i + 2][1]
        word6 = sent[i + 3][0]
        postag6 = sent[i + 3][1]
        features.update({
            '-1:postag': postag1,
            '-1:word': word1,
	    '-2:postag': postag2,
            '-2:word': word2,
	    '-3:postag': postag3,
            '-3:word': word3,
            '+1:postag': postag4,
            '+1:word': word4,
	    '+2:postag': postag5,
            '+2:word': word5,
	    '+3:postag': postag6,
            '+3:word': word6,
	    '-1:suffix': word1[-3:],
	    '-2:suffix': word2[-3:],
	    '-3:suffix': word3[-3:],
	    '+1:suffix': word4[-3:],
	    '+2:suffix': word5[-3:],
	    '+3:suffix': word6[-3:],
	
        })

    
    
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
    fread=open("dev_corpus_train_PROC.txt","r")
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
    
    crf.fit(X_train, y_train)

    labels = list(crf.classes_)
    labels.remove('O')
    print labels
    
    y_pred= crf.predict(X_test)

    print("Top positive:")
    print_state_features(Counter(crf.state_features_).most_common(30))

    print("\nTop negative:")
    print_state_features(Counter(crf.state_features_).most_common()[-30:])
    print metrics.flat_f1_score(y_test, y_pred,
                      average='weighted', labels=labels)

    for i in range(len(y_pred)):
	print "??"*20
	print y_pred[i],len(y_pred[i])
	print "&&"*20
	print y_test[i],len(y_pred[i])
	print "**"*20
	print test_sents[i]
	
	raw_input()
	
    #print y_print metrics.flat_f1_score(y_test, y_pred,average='weighted', labels=labels)

createdata()
