# -*- coding: utf-8 -*-
"""2017.3.14 
判讀抓取下來的特徵詞的讀音計算次數
2017.3.28 跟著grab更新
"""

import os

tone_ = ['do2', 'e3-sai4', 'ggau2', 'giann2', 'hang2', 'hing2', 'hing7', 'zua7']
trainNum = ['1991', '1992', '1993', '1994', '1995', '1996', '1997']
grabMethodList = ['nb', 'allhead', 'tree_nb']
ctsMethodList = ['fullcts', 'subcts']
tonelist = []
toneDictList = []

# user
readPath = '../data/grablist/output'
writePath = '../data/training/output'

# toneDictList 的建立
for fileNum in trainNum:
    with open(f'../data/input/{fileNum}out.txt', 'r', encoding = 'utf8') as fr:
        lines = fr.readlines()
    tonelist.append(lines)
for item in tonelist:
    toneDictList.append({item[2+4*k].split()[0]:item[3+4*k].split()[1]
                         for k in range(int(len(item)/4))})

# 開檔
readNameList = os.listdir(readPath)
for n, i in enumerate(os.listdir(readPath)):
    print(n, ' ', i)
readName = readNameList[int(input('Please input file number:'))]
with open(os.path.join(readPath, readName), 'r', encoding='utf8') as fr1:
    words = fr1.readlines()

writeName = os.path.splitext(readName)[0]+'(tone).txt'
with open(os.path.join(writePath, writeName), 'w') as fw:
    for word in words[1:]:
        index = word.split()[0]
        fw.write(word.split(',')[0][:-4])  # index & freq
        freq = word.split()[1]
        try:
            tone = word.split()[2]
        except:
            print(index)
        tone = tone.split('|')[:-1]

        tonelist = [0,0,0,0,0,0,0,0]  # 存每一句有甚麼音
        for tp in tone:
            tp = tp.split(',')
            f_num = tp[0]
            num = tp[1]
            tone = toneDictList[trainNum.index(f_num)].get(num)
            try:
                tonelist[tone_.index(tone)] += 1
            except:
                print(index, f_num, num)
        fw.write(str(tonelist) + '\n')
print('finish')             
        


    

