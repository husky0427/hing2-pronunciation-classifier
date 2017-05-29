# -*- coding: utf-8 -*-
"""
Created on Tue Mar 28 21:01:21 2017

算分數
"""
from strprc import no_abc123, no_chinese

tone_ = ['do2', 'e3-sai4', 'ggau2', 'giann2', 'hang2', 'hing2', 'hing7', 'zua7']
freq_ = [5, 433, 3, 3383, 203, 5642, 2, 14]

class Score:
    def __init__(self, List, tone):  #List is 分數
        if isinstance(List, str):
            self.score = 'no feature'
        elif List == [0, 0, 0, 0, 0, 0, 0, 0]:
            self.score = 'inapplicable'
        else:
            self.score = [round(_, 2) for _ in List]
            self.correctList1 = [0, 0]  # 正確 & 錯誤
            self.correctList2 = [0, 0]  #不算一次 正確 & 錯誤
            self.tone = tone # 正確讀音
            self.toneNum = tone_.index(self.tone) # 正確讀音Num
            self.toneScore = self.score[self.toneNum]  # 正確讀音的分數
            self.rank = sorted(self.score,reverse=1).index(self.toneScore)+1 # 正確讀音排第幾    
            self.allrank = len(set(self.score))  # 全部共有幾名
            self.predictone = predictone(self.score)  # 預測的讀音
            self.spFault = [0, 0]
    def judge(self, fList, _1List): #  feature, 出現一次List
        chList = [no_abc123(tp[1]) for tp in fList]
        if self.predictone == self.tone:
            self.correctList1[0] = 1
            if any(k not in _1List for k in chList):
                self.correctList2[0] = 1
        else:
            self.correctList1[1] = 1
            if any(k not in _1List for k in chList):
                self.correctList2[1] = 1
            # 特殊錯誤
            if max(self.score)-self.score[self.toneNum] < sum(self.score)/5:
                self.spFault[0] = 1
            if 3 < self.rank:
                self.spFault[1] = 1
        return self.correctList1 + self.correctList2 + self.spFault  
    # for combined by file(no _1List)
    def judge2(self):  # feature List
        if self.predictone == self.tone:
            self.correctList1[0] = 1
        else:
            self.correctList1[1] = 1
            # 特殊錯誤
            if max(self.score)-self.score[self.toneNum] < sum(self.score)/5:
                self.spFault[0] = 1
            if 3 < self.rank:
                self.spFault[1] = 1
        return self.correctList1 + self.spFault
# 預測讀音
def predictone(score):
    fitList = [i  for i, n in enumerate(score) if n == max(score)]
    _max = max([freq_[i] for i in fitList])
    return tone_[freq_.index(_max)]
 # main function
if __name__ == '__main__':
    pass
    
            
            
        