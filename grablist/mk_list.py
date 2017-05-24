"""2017.3.8
python version :3.6.1

製作grab下來的training資料擷取整理
以詞語當index

2017.3.20
新增 單層dpds
"""
import re
from collections import defaultdict

import grab4 as grab
from strprc import no_abc123, no_chinese

trainNum = ['1991', '1992', '1993', '1994', '1995', '1996', '1997']
grabMethodList = ['nb', 'allhead', 'treenb']
ctsMethodList = ['fullcts', 'subcts']
layerNum = ''
layerNumStr = ''

dataDict = defaultdict(list)  # 資料存放的dict
cnt = 0
posi = []
                      
# 計算中文字數(對齊用)
def len_ch(data):
    temp = re.findall('[^a-zA-Z0-9.]+', data)
    count = 0
    for i in temp:
        count += len(i)
    return(count)


# user 
grabMethod = input('Please input 1:nb 2:allhead 3:tree nb:')
ctsMethod = input('Please input 1:fullcts 2:subcts:')
grabMethod = grabMethodList[int(grabMethod)-1]
ctsMethod = ctsMethodList[int(ctsMethod)-1]

# 輸入position
while 'x' not in posi:
    posi.append(input(f'Please input position{posi}:'))
posi.pop()  # 拿掉x
if len(posi) == 1:
    posiName = posi[0]
else:
    posiName = 'other'    
posi = [int(i) for i in posi]  # 轉成數字                    

            
# make dict
for fileNum in trainNum:
    with open(f'../data/grablist/input/{fileNum}{ctsMethod}.txt', 'r', encoding = 'utf8') as fr:
        lines = fr.readlines()
    lines = lines[:int(len(lines)/2)]  # 只取訓練資料的前半
    
    for line in lines:
        num = line.split()[0]  # @num
        st = line.split()[1]
        content = grab.Grab(st)
        if grabMethod == grabMethodList[0]:   
            feature = content.nb(*posi)
        elif grabMethod == grabMethodList[1]:
            feature = content.all_head(*posi)
        elif grabMethod == grabMethodList[2]:
            if layerNum == '':
                layerNum = input('Please input layerNum:')
            feature =  content.tree_nb(int(layerNum), *posi)
            layerNumStr = '('+str(layerNum)+')'

       
        for tp in feature:  # tuple:(1, 'DET:一')7
            position = tp[0]
            ch = no_abc123(tp[1])
            dataDict[ch].append((fileNum, num, position))
            
    sortDataList = sorted(dataDict.items(),
                    key = lambda w: len(w[1]), reverse = True)  # 排序字典
            
    with open(f'../data/grablist/output/{grabMethod}{layerNumStr}_{ctsMethod}_{posiName}.txt','w',encoding='utf8') as fw:
        fw.write(str(posi) + '\n')
        for word in sortDataList:
            w = word[0]
            l = len_ch(w)  # 計算中文字數
            w = w.ljust(21-l)
            fw.write(w)
            tpList = word[1]
            cnt = cnt + len(tpList)
            lenth = str(len(tpList)).ljust(6)
            fw.write(lenth)
            for tp in tpList:
                fw.write(str(tp[0])+','+str(tp[1])+','+str(tp[2])+'|')
            fw.write('\n')    
print('finish!')        
            
        
            
