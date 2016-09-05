import sys,os
from nltk.tokenize import sent_tokenize



def runner(directory = "../tagged_text/"):

    files = os.listdir(directory)
    for file in files:
        ff=open(directory+file,"r")
        contents=ff.readlines()
        fw=open(directory.replace("tagged_text","tokenised_text")+file,"w+")
        for lines in contents:
            print lines.decode("utf-8")
            results=sent_tokenize(lines.decode("utf-8"))
            for i in results:
                #print i
                print>>fw,(i.encode('utf-8'))



runner()