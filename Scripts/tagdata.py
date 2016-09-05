#substitutes the only text with tags
import sys,os,re
from nltk.tokenize import TreebankWordTokenizer
#issue
#When there are multiple places where same word occurs they should be tagged uniquely
#For ex when we have n-alkanes and homologenous n-alkanes we tag as n-alkanes=U-MAT and homologenous=B-MAT and n-alkanes=U-MAT
#
def tagdata():
    directory = "../tagged_annotation/"
    files = os.listdir(directory)
    fwrite = open("../tagged_text/dev_corpus.txt", "w+")
    for file in files:
        print file
        ff = open(directory + file, "r")
        contents = ff.readlines()
        ftext =open("../text/" + file.replace(".ann",".txt"), "r",)
        line=ftext.read()


        tempdict={}
        for annotation in contents:
            #print "annotation in progress"
            annotation=annotation.split("||")
            key=annotation[1].split("\n")[0]
            value=" ".join(annotation[0].split()[4:])
            tempdict[key]=value
            #print key,"----",value
        for key,value in tempdict.items():
            print key,value
            line=line.replace(key,value)

        print line
        tokenizer = TreebankWordTokenizer()
        #line=line.split()
        line=tokenizer.tokenize(line)
        for i in range(len(line)):
            if "|" not in line[i]:
                line[i]=line[i]+"|O"

        #print " ".join(line)
        print>>fwrite," ".join(line)

tagdata()