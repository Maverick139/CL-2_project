#!/usr/bin/env python
# coding: utf-8

def run(filepath):    # READING FROM FILE + CLEANING + CREATING LIST(sent) OF LIST(words) DICT(attr)

    #filepath = 'pos_output.txt' #READING
    fp = open(filepath)
    line = fp.readline()

    lld = []    
    lld.append([])
    sent_index=0
    word_index=0

    while line:
        sent = line.split('\t') #CLEANING

        # <Improper Case>
        if(sent[0]=="<s>" or sent[0]=="</s>" or sent[0]=="<s>\n" or sent[0]=="</s>\n"):
            line = fp.readline()
            continue
        if(sent[0]=="."):
            sent_index+=1
            word_index=0
            lld.append([])  #new sentence
            line = fp.readline()
            continue
        # </Improper Case>

        # print(sent[2])  
        # <Proper Case>     #CREATING LLD
        lld[sent_index].append([])  # new word
        lld[sent_index][word_index] = {}
        lld[sent_index][word_index]["tok"] = sent[0]
        lld[sent_index][word_index]["pos"] = sent[2]
        lld[sent_index][word_index]["gen"] = sent[5]
        lld[sent_index][word_index]["num"] = sent[6]

        word_index+=1
        # </Proper Case>

        line = fp.readline()

    #print(lld)
    return lld