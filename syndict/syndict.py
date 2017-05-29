# -*- coding: utf-8 -*-
"""
Created on Sun May 14 17:14:03 2017

load syn

@author: speechlab
"""


from collections import defaultdict

class syn_dict(trainDict):
    def __init__(self, trainDict):
        self.synDict2 = defaultdict(list)
        self.synDict3 = defaultdict(list)
        with open('./dict.txt', encoding='utf') as fr:
            ori = fr.readlines()  # original data of synDict
        for line in ori:
            if '[' in line:  # is chinese
                index = line.split(' [')
                wordSet = line.split('[ ')[1].split('  ]')[0].split(' , ')
                # make synDict2
                if index in trainDict.keys():
                    for word in wordSet:
                        self.synDict2[word].append(index)
                # make synDict3
                for word in wordSet:
                    for elem in wordSet:
                        self.synDict3[word].append(elem)
                    
