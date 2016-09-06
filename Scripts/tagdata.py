#substitutes the only text with tags
import sys,os,re,codecs
from nltk.tokenize import TreebankWordTokenizer
from nltk.tokenize import StanfordTokenizer
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
        ff = codecs.open(directory + file, "r","utf-8")
        contents = ff.readlines()
        ftext =codecs.open("../text/" + file.replace(".ann",".txt"), "r","utf-8")
        line=ftext.read()


        tempdict={}
        '''
        for annotation in contents:
            annotation = annotation.split("||")
            key = annotation[1].split("\n")[0]
            start=(annotation[0].split(" ")[2])
            end=(annotation[0].split(" ")[3])
            tempdict[start+"||"+end] = " ".join(annotation[0].split()[4:])
        liness = line
        imp=0

        for key, value in tempdict.items():
            # print key,value
            #print value

            start=int(key.split("||")[0])
            end=int(key.split("||")[1])
            oldlen=len(line[start:end])
            newlen=len(value)
            imp=newlen-oldlen
            firstpart=liness[:start]
            secondpart=liness[end:]
            liness=firstpart+" "+value+" "+secondpart
            #print liness[start:end],value,start,end,
             #line=line.replace(key,value)
            #line = re.sub(r"\b%s\b" % key, value, line)
        '''
        for annotation in contents:
            #print "annotation in progress"
            annotation=annotation.split("||")
            key=annotation[1].split("\n")[0]
            value=" ".join(annotation[0].split()[4:])
            tempdict[key]=value
            #print key,"----",value
        for key,value in tempdict.items():
            #print key,value
            #line=line.replace(key,value)
            line=re.sub(r"\b%s\b" % key, value, line)

        #print os.environ['CLASSPATH']
        #tokenizer = StanfordTokenizer()
        #line=line.split()
        line=re.split(r"[^\w\|\-]",line)
        #line=tokenizer.tokenize(line)
        print line

        ''''
        print liness
        print line
        liness=liness.strip()
        liness = re.split(r"[^\w\|\-]", liness)
        for i in range(len(liness)):
            if "|" not in liness[i]:
                liness[i]=liness[i]+"|O"

        #print " ".join(line)
        #print>>fwrite," ".join(line)
        '''
        for i in range(len(line)):
            if "|" not in line[i]:
                line[i] = line[i] + "|O"
        print line
        print>>fwrite," ".join(line)
tagdata()