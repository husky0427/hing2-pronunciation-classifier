# -*- coding: utf-8 -*-
"""
Created on Sun May 14 17:14:03 2017

load syn

@author: speechlab
"""


from collections import defaultdict

class syn_dict:
    def __init__(self, trainDict, dic='ehownet'):
        self.trainDict = trainDict
        if dic == 'ehownet':
            self.synDict2 = {}
            self.synDict3 = defaultdict(list)
            self.synDict4 = defaultdict(list)
            self.syn2trainDict = {}
            with open('./dict.txt', encoding='utf') as fr:
                ori = fr.readlines()  # original data of synDict
            for line in ori:
                if '[' in line:  # is chinese
                    index = line.split(' [')[0]
                    wordSet = line.split('[ ')[1].split('  ]')[0].split(' , ')
                    if index in wordSet:  # 移除在wordSet中和index相同的詞
                        wordSet.remove(index)
                    intersec = set(trainDict.keys()) & set(wordSet)  # intersection
                    # make synDict3
                    if index in self.trainDict.keys():
                        for word in wordSet:
                            self.synDict3[word].append(index)
                    # make synDict4, synDict2
                    if not len(intersec):  # if intersection == 0
                        continue
                    self.synDict2[index] = intersec
                    for word in wordSet:
                        self.synDict4[word] += list(intersec-set([word]))  
        
        elif dic == 'wordforest1':  # 一行為一組
            self.synDict4 = defaultdict(list)
            with open('./wordforest.txt', encoding='utf') as fr:
                ori = fr.readlines()  # original data of synDict
            for line in ori:
                if '=' in line or '#' in line:
                    wordSet = line.split()[1:]
                    intersec = set(trainDict.keys()) & set(wordSet)  # intersection
                    if not len(intersec):  # if intersection == 0
                        continue
                    for word in wordSet:
                        self.synDict4[word] += list(intersec-set([word]))

                        
        elif dic == 'wordforest2':  # 同類為一組
            self.synDict4 = defaultdict(list)
            tempDict = defaultdict(list)
            with open('./wordforest.txt', encoding='utf') as fr:
                ori = fr.readlines()  # original data of synDict
            for line in ori:
                taxonomy = line.split()[0][0:5]
                wordSet = line.split()[1:]
                tempDict[taxonomy] += wordSet
            wordSets = tempDict.values()
            for Set in wordSets:
                intersec = set(trainDict.keys()) & set(Set)  # intersection
                if not len(intersec):  # if intersection == 0
                        continue
                for word in Set:
                    self.synDict4[word] += list(intersec-set([word]))
                
                
    # input為詞，取得分數
    def get_score(self, word, scoreNum, dictSwitch=1):
        if dictSwitch == 1:
            try:
                return self.trainDict[word][scoreNum-1]
            except:
                return [0, 0, 0, 0, 0, 0, 0, 0]
            
        if dictSwitch == 2:
            score = [0, 0, 0, 0, 0, 0, 0, 0]
            try:
                tempList = self.synDict2[word]
            except:
                return [0, 0, 0, 0, 0, 0, 0, 0]
            for item in tempList:
                tempscore = self.trainDict[item][scoreNum-1]
                score = [a + b for a, b in zip(score, tempscore)]
            score = [round(i/len(tempList), 2) for i in score]
            return score
                
        if dictSwitch == 3:
            score = [0, 0, 0, 0, 0, 0, 0, 0]
            if word in self.synDict3:
                indexList = self.synDict3[word]
            for index in indexList:
                try:
                    temp = self.trainDict[index][scoreNum-1]  # 單一index的score
                except KeyError:
                    temp = [0, 0, 0, 0, 0, 0, 0, 0]
                score = [a + b for a, b in zip(score, temp)]
            score = [round(i/len(indexList), 2) for i in score]
            return score
        
        if dictSwitch == 4:
            score = [0, 0, 0, 0, 0, 0, 0, 0]
            if word in self.synDict4:
                targetList = self.synDict4[word]
            for target in targetList:
                try:
                    temp = self.trainDict[target][scoreNum-1]  # 單一target的score
                except:
                    temp = [0, 0, 0, 0, 0, 0, 0, 0]
                score = [a + b for a, b in zip(score, temp)]
            score = [round(i/len(targetList), 2) for i in score]
            return score
        
        if dictSwitch == 5:  # 2+3
            score = [0, 0, 0, 0, 0, 0, 0, 0]
            try:
                tempList = self.synDict2[word]
            except:
                tempList = []
            for item in tempList:
                tempscore = self.trainDict[item][scoreNum-1]
                score = [a + b for a, b in zip(score, tempscore)]
            try:
                indexList = self.synDict3[word]
            except KeyError:
                indexList = []
            for index in indexList:
                try:
                    temp = self.trainDict[index][scoreNum-1]  # 單一index的score
                except KeyError:
                    temp = [0, 0, 0, 0, 0, 0, 0, 0]
                score = [a + b for a, b in zip(score, temp)]
            score = [round(i/(len(indexList)+len(tempList)), 2) for i in score]
            return score
            
            