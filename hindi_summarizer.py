#!/usr/bin/env python
# coding: utf-8

import preprocessor
import operator
import heapq
from collections import Counter
import math

"""
0.take input parameters
1.POS tag (pos tagged file generated) # SIVA REDDY
2.process pos tagged file (lld generated)
3.calculate frequnetial score
4.calculate word score
4.calculate referrential score
5.calculate cummulative score
6.Render summary
"""
def sigmoid(x):
  return 1 / (1 + math.exp(-x))

def w_lev_rel(c_id, s_id, p_id, local_word_score, word_score, lld):
    val = 0
    temp = 0
    nonstop = ["NN", "NNP", "JJ", "RB", "XC", "QC"]
    for word1 in lld[s_id]:
        if(word1["tok"] not in word_score or word1["tok"] not in local_word_score[c_id-1]):
            continue
        for word2 in lld[p_id]:
            if(word2["tok"] not in word_score or word2["tok"] not in local_word_score[c_id-1]):
                continue
            if(word1["tok"]==word2["tok"] and word1["pos"] in nonstop):
                val += local_word_score[c_id-1][word1["tok"]]/word_score[word1["tok"]]
    if(val<0.1):
        val=0.1
    # print(val)
    return val

def calculate_word_score(lld):
    nonstop = ["NN", "NNP", "JJ", "RB", "XC", "QC"]
    wdfq = {}
    for sent in lld:
        for word in sent:
            if(word["tok"] not in wdfq):
                if(word["pos"] in nonstop):
                    wdfq[word["tok"]] = 1
            else:
                if(word["pos"] in nonstop):
                    wdfq[word["tok"]] +=1
    return wdfq

def cluster_belonging(c_id, s_id, local_word_score, word_score, lld):
    sigma = 0;
    k=1
    i = lld[s_id]   # i: list(word) of dict(attr)
    for j in forest[c_id-1]:    # j = forest[c_id][nth](sentence) : dict{s_id, score, list(word) of dict(attr)}
        dist = s_id - j["s_id"]
        heirarchical_factor = j["score"]
        w_level_relation = w_lev_rel(c_id, s_id, j["s_id"], local_word_score, word_score, lld)
        sigma += k*heirarchical_factor*w_level_relation/dist
        k*=0.8
    return sigma

def coherence_factor(s_id, lld):
    delta = 1
    ref_count = 1
    exceptions = ["आप","आपका","आपकी","आपको","आपके","आपने","हमारा","हमारी","हमारे","हमे","हमने","हमको","हम","हमसे","आपसे"]
    for i in range(len(lld[s_id])): #ith word"
        word = lld[s_id][i]
        if(i==0):
            if(word["tok"] not in exceptions and (word["pos"]=="PRP" or word["pos"]=="DEM")):
                delta /= 100000
                ref_count += 1
            elif(word["tok"] in exceptions):
                delta = 2
        else:
            if(word["tok"] not in exceptions and (word["pos"]=="PRP" or word["pos"]=="DEM")):
                ref_count += 1
    delta /= ref_count
    # print("ref",ref_count)
    return sigmoid(delta)

def update_lwscr(c_id, s_id, local_word_score, lld):
    nonstop = ["NN", "NNP", "JJ", "RB", "XC", "QC"]
    for word in lld[s_id]:
        if(word["pos"] in nonstop):
            if(word["tok"] in local_word_score[c_id]):
                local_word_score[c_id][word["tok"]] +=1
            else:
                local_word_score[c_id][word["tok"]] = 1
    return local_word_score

def coherence_filter(forest, lld):
    for cluster in forest:
        for sent in cluster:
            cf = coherence_factor(sent["s_id"], lld)
            if(cf < 0.6):
                cluster.remove(sent)
    return forest

lld = preprocessor.run('pos_output.txt')
s_count = len(lld)-1
word_score = calculate_word_score(lld)
local_word_score = []
forest = []
cluster_count = 0
s_id =0
for sent in lld:

    if(s_id==0):
        forest.append([])
        local_word_score.append({})
        forest[cluster_count].append({"s_id":s_id, "score":1, "sent":sent})
        local_word_score = update_lwscr(cluster_count, s_id, local_word_score, lld)
        cluster_count+=1
        s_id+=1
        continue

    referrential_score = cluster_belonging(cluster_count, s_id, local_word_score, word_score, lld)
    coherence_score = coherence_factor(s_id, lld)
    final_score = sigmoid(referrential_score/coherence_score)

    if(final_score > 0.52): # greater the const, more the number of clusters
        forest[cluster_count-1].append({"s_id":s_id, "score":final_score, "sent":sent})
        local_word_score = update_lwscr(cluster_count-1, s_id, local_word_score, lld)
    else:
        forest.append([])
        local_word_score.append({})
        local_word_score = update_lwscr(cluster_count, s_id, local_word_score, lld)
        # print("NEW CLUSTER")
        forest[cluster_count].append({"s_id":s_id, "score":1, "sent":sent})
        cluster_count+=1

    s_id+=1

# for cluster in forest:
#     for sent in cluster:
#             print(sent)

forest = coherence_filter(forest, lld)

per = 30

for cl in range(len(forest)):
    cluster = forest[cl]
    if(cl==len(forest)-2):
        for s in range(int(len(cluster)*(100-1.5*per)/100), len(cluster)):
            sent = cluster[s]
            for word in sent["sent"]:
                print(word["tok"], end=" ")
            print("।")

    elif(cl==0):   
        for s in range(0, int(len(cluster)*1.5*per/100)):
            sent = cluster[s]
            for word in sent["sent"]:
                print(word["tok"], end=" ")
            print("।")

    else:   
        for s in range(0, int(len(cluster)*per/100)):
            sent = cluster[s]
            for word in sent["sent"]:
                print(word["tok"], end=" ")
            print("।")