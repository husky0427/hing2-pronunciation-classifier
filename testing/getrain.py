# -*- coding: utf-8 -*-
"""
testing中讀取training資料

@author: speechlab
"""

class Training:
    
    def __init__(self, readPath, readName):
        self._1List = []  # 只出現一次的word
        self.trainDict = {}
        with open(os.path.join(readPath, readName), 'r') as fr:
            words = fr.readlines()
        for word in words:
            index = word.split()[0]
            freq = int(word.split()[1])
            score = word.split('[')[1].split(']')[0]
            score = score.split(', ')
            scoreList1 = [int(n)/freq for n in score]  # 比例
            scoreList2 = [int(n) for n in score]  # 次數
            scoreList3 = [round(math.log2(1+n), 2) for n in scoreList2]  # 次數log
            self.trainingDict[index] = scoreList1, scoreList2, scoreList3
            if freq == 1:
                self._1List.append(index)
    def onetimelist(self):
        return self._1List
    def getscore1(self, word):
        return self.trainDict.get(word)[0]
    def getscore2(self, word):
        return self.trainDict.get(word)[1]
    def getscore3(self, word):
        return self.trainDict.get(word)[2]
    