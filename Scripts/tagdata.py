#substitutes the only text with tags
import sys,os,re

def tagdata():
    directory = "../tagged_annotation/"
    files = os.listdir(directory)
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
            line=line.replace(key,value)
        print line

tagdata()