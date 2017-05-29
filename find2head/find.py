# -*- coding: utf-8 -*-
"""
找出句中有雙Head的

@author: speechlab
"""

import os
import glob
from grab4 import tree

fw = open('./result.txt', 'w', encoding='utf8')
path = './*.txt'
fileList = glob.glob(path)
for n,file in enumerate(fileList):
    with open(file, 'r', encoding='utf8') as f:
        lines = f.readlines()
    lines = lines[:int(len(lines)/2)]
        
    for line in lines:
        num = line.split()[0]
        st = line.split()[1].split('#')[0]
        out = Grab(st)
        try:
            T = tree(st)
            PList = T.productions()
            for item in PList:
                temp = str(item).split('-> ')[1].split()
                cnt = 0
                for i in temp:
                    if 'Head' in i:
                        cnt += 1
                        if cnt > 1:
                            fw.write(f'{os.path.split(file)[1]}__{num}__{item}\n')
                            break
        except:
            pass                        