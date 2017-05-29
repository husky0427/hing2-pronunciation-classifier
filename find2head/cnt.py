# -*- coding: utf-8 -*-
"""
統計2head出現次數

@author: speechlab
"""
from collections import defaultdict

pDict= {}

with open('./result.txt', 'r', encoding='utf8') as f:
    lines = f.readlines()

for line in lines:
    p = line.split('__')[-1]
    if p in pDict:
        pDict[p] = pDict[p] + 1
    else:
        pDict[p] = 1
        
sortpList = sorted(pDict.items(), key = lambda d:d[1], reverse = True)  # 排序字典

with open('./cnt.txt', 'w', encoding='utf8') as fw:
    for item in sortpList:
        fw.write(f'{item[0][:-1].ljust(40)}{item[1]}\n')
    