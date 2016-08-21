from collections import Counter
import re,sys,os


def openfile(filename):
    fh = open(filename, "r+")
    str = fh.read()
    fh.close()
    return str


def removegarbage(str):
    # Replace one or more non-word (non-alphanumeric) chars with a space
    str = re.sub(r'\W+', ' ', str)
    str = str.lower()
    return str


def getwordbins(words,cnt):
    for word in words:
        cnt[word] += 1
    return cnt


def extract(filename, cnt,topwords=10):
    txt = openfile(filename)
    txt = removegarbage(txt)
    words = txt.split(' ')
    counter = getwordbins(words,cnt)
    return  counter

def main():
    files=os.listdir("../text")
    cnter=Counter()
    for filename in files:
        cnter=extract("../text/"+filename,cnter)
    print len(cnter)
    for key in ((cnter).most_common(1000)):
        print key, cnter[key]

main()