# -*- coding: utf-8 -*-
"""2017.3.15

@author: husky0427
2017.3.28 隨grab修改更新

"""
import os
import math

import grab4 as grab
import score as scorecalcu
import syndict
from strprc import no_abc123, no_chinese


tone_ = ['do2', 'e3-sai4', 'ggau2', 'giann2', 'hang2', 'hing2', 'hing7', 'zua7']
trainNum = ['1991', '1992', '1993', '1994', '1995', '1996', '1997']

def percent(a, b): # 分子分母
    return round(a/b,4)*100

# global variable
start = 5  # 檔案開始
end = 6  # 檔案結束
dictswitch = 4  # synDict Switch
Dic = 'wordforest2'


def testing(readPath, writePath, readName):
    # user
    writeName = readName[:-10] + '(test).txt'
    writeNameRp1 = readName[:-10] + '(testRp1).txt'
    writeNameRp2 = readName[:-10] + '(testRp2).txt'
    ctsMethod = readName[:-10].split('_')[1]
    grabMethod = readName[:-10].split('_')[0].split('(')[0]
    posi = [int(readName[:-10].split('_')[2])]

    # initial
    trainingDict = {}
    _1List = []  # 只出現一次的詞
    cnt = 0
    v = [0, 0, 0]  # 正確
    x = [0, 0, 0]  # 錯誤
    noFind = 0
    v1 = [0, 0, 0]  # (不計入training只有一次的) 
    x1 = [0, 0, 0]
    inappli = 0  # inapplicable
    
    
    # loading training data
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
        trainingDict[index] = scoreList1, scoreList2, scoreList3
        if freq == 1:
            _1List.append(index)
    # syndict
    syn = syndict.syn_dict(trainingDict, dic=Dic)

    
    # 寫檔
    fw = open(os.path.join(writePath,writeName), 'w', encoding = 'utf8')
    fw_report1 = open(os.path.join(writePath,writeNameRp1),'w', encoding = 'utf8')
    fw_report2 = open(os.path.join(writePath,writeNameRp2),'w', encoding = 'utf8')
    # toneDict
    for fileNum in trainNum:
        with open(f'../data/input/{fileNum}out.txt', 'r', encoding = 'utf8') as fr1:
            toneFile = fr1.readlines()
        toneDict = {toneFile[2+4*k].split()[0]:toneFile[3+4*k].split()[1]
                         for k in range(int(len(toneFile)/4))}    
        # test
        with open(f'../data/grablist/input/{fileNum}{ctsMethod}.txt', 'r', encoding = 'utf8') as fr2:
            lines = fr2.readlines()
        lines = lines[int(len(lines)*start/10)+1:int(len(lines)*end/10)]  # 只取資料的前半
    
        for line in lines:
            ch = ''  # 初始化
            cnt += 1
            t_score1 = [0,0,0,0,0,0,0,0]  # 分數計算初始化
            t_score2 = [0,0,0,0,0,0,0,0]
            t_score3 = [0,0,0,0,0,0,0,0]
            num = line.split()[0]  # @num
            st = line.split()[1]
            tone = toneDict.get(num)  # 正確讀音
            fw.write('\n'+fileNum.ljust(7)+num.ljust(7)+'\n'+st+'\n')
            content = grab.Grab(st)
            if grabMethod == 'nb':
                feature = content.nb(*posi)
            elif grabMethod == 'allhead':
                feature = content.all_head(*posi)
            elif grabMethod == 'treenb':
                layerNum = readName.split('(')[1].split(')')[0]
                feature =  content.tree_nb(int(layerNum), *posi)
            # 若該方法沒有特徵詞    
            if feature == []:  
                noFind += 1
                fw.write('[]\n')
                fw.write('no feature'.ljust(50)+ tone + '\n')  # 正確讀音
                fw.write('no feature'.ljust(50)+ tone + '\n')  # 正確讀音
                fw.write('no feature'.ljust(50)+ tone + '\n')  # 正確讀音
            else:
                fw.write(str(feature) + '\n')
                for tp in feature:  # tuple:(1, 'DET:一')7
                    ch = no_abc123(tp[1])
                    p = tp[0]
                    try:
                        sc1 = syn.get_score(ch, scoreNum=1, dictSwitch=dictswitch)
                        t_score1 = [round(a+b,2) for a,b in zip(sc1, t_score1)]
                        sc2 = syn.get_score(ch, scoreNum=2, dictSwitch=dictswitch)
                        t_score2 = [a+b for a,b in zip(sc2, t_score2)]
                        sc3 = syn.get_score(ch, scoreNum=3, dictSwitch=dictswitch)
                        t_score3 = [a+b for a,b in zip(sc3, t_score3)]                   
                    except:
                        pass
                # 判斷是否為inapplicable (全為0)
                if t_score1 == [0, 0, 0, 0, 0, 0, 0, 0]:
                    inappli += 1
                    fw.write('inapplicable'.ljust(50) + tone + '\n')
                    fw.write('inapplicable'.ljust(50) + tone + '\n')
                    fw.write('inapplicable'.ljust(50) + tone + '\n')
                    continue
                # 分數1
                s1 = scorecalcu.Score(t_score1, tone)
                correctList = s1.judge(feature, _1List)
                v[0] = v[0] + s1.correctList1[0]
                x[0] = x[0] + s1.correctList1[1]
                v1[0] = v1[0] + s1.correctList2[0]
                x1[0] = x1[0] + s1.correctList2[1]
                if s1.spFault[0] == 1:
                    fw_report1.write('s1 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report1.write(tone.ljust(8)+s1.predictone.ljust(8))  # 第一種錯誤紀錄
                    fw_report1.write(str(feature).ljust(30) + '\n')
                if s1.spFault[1] == 1:
                    fw_report2.write('s1 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report2.write(tone.ljust(8)+s1.predictone.ljust(8))  # 第二種錯誤紀錄
                    fw_report2.write(str(feature).ljust(30) + '\n')                
                fw.write(str(t_score1).ljust(50) + tone.ljust(8) + str(s1.rank) + '/'
                     + str(s1.allrank) + '\n')
                # 分數2
                s2 = scorecalcu.Score(t_score2, tone)
                correctList = s2.judge(feature, _1List)
                v[1] = v[1] + s2.correctList1[0]
                x[1] = x[1] + s2.correctList1[1]
                v1[1] = v1[1] + s2.correctList2[0]
                x1[1] = x1[1] + s2.correctList2[1]
                if s2.spFault[0] == 1:
                    fw_report1.write('s2 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report1.write(tone.ljust(8)+s2.predictone.ljust(8))  # 第一種錯誤紀錄
                    fw_report1.write(str(feature).ljust(30)+ '\n')
                if s2.spFault[1] == 1:
                    fw_report2.write('s2 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report2.write(tone.ljust(8)+s2.predictone.ljust(8))  # 第二種錯誤紀錄
                    fw_report2.write(str(feature).ljust(30)+ '\n')                
                fw.write(str(t_score2).ljust(50) + tone.ljust(8) + str(s2.rank) + '/'
                     + str(s2.allrank) + '\n')
                # 分數3
                s3 = scorecalcu.Score(t_score3, tone)
                correctList = s3.judge(feature, _1List)
                v[2] = v[2] + s3.correctList1[0]
                x[2] = x[2] + s3.correctList1[1]
                v1[2] = v1[2] + s3.correctList2[0]
                x1[2] = x1[2] + s3.correctList2[1]
                if s3.spFault[0] == 1:
                    fw_report1.write('s3 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report1.write(tone.ljust(8)+s3.predictone.ljust(8))  # 第一種錯誤紀錄
                    fw_report1.write(str(feature).ljust(30)+ '\n')
                if s3.spFault[1] == 1:
                    fw_report2.write('s3 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report2.write(tone.ljust(8)+s3.predictone.ljust(8))  # 第二種錯誤紀錄
                    fw_report2.write(str(feature).ljust(30) + '\n')                
                fw.write(str(t_score3).ljust(50) + tone.ljust(8) + str(s3.rank) + '/'
                     + str(s3.allrank) + '\n')

    try:
        prec = [format(round(t/(t+f),5)*100, '.3f') for t, f in zip(v, x)]  # 一次有算 
        prec1 = [format(round(t/(t+f),5)*100, '.3f') for t, f in zip(v1, x1)]  # 一次不算
    except ZeroDivisionError:
        prec, prec1 = [0,0,0], [0,0,0]
    applicRate = format(round((cnt-noFind-inappli)/cnt,5)*100, '.3f') 
        
    fw.write(f'\n\n共{cnt}句, no feature:{noFind}, inapplicable:{inappli}, applicability:{applicRate}%\n')
    fw.write(f'\nS1 正確:{v[0]}, 錯誤:{x[0]}, precision:{prec[0]}%\n')
    fw.write(f'不算詞頻為1的特徵詞 正確:{v1[0]} 錯誤:{x1[0]}  precision:{prec1[0]}%\n' )
    fw.write(f'\nS2 正確:{v[1]}, 錯誤:{x[1]}, precision:{prec[1]}%\n')
    fw.write(f'不算詞頻為1的特徵詞 正確:{v1[1]} 錯誤:{x1[1]} precision:{prec1[1]}%\n') 
    fw.write(f'\nS3 正確:{v[2]}, 錯誤:{x[2]}, precision:{prec[2]}%\n')
    fw.write(f'不算詞頻為1的特徵詞 正確:{v1[2]} 錯誤:{x1[2]} precision:{prec1[2]}%\n')        
    fw.close()        
    fw_report1.close()
    fw_report2.close()
    return cnt, noFind, inappli, applicRate, prec, prec1
    print('finish')         
             

# main function        
if __name__ == "__main__":
    readPath = '../data/training/output'
    writePath = '../data/testing/output'
    readNameList = os.listdir(readPath)
    for n, i in enumerate(os.listdir(readPath)):
        print(n, ' ', i)
    readName = readNameList[int(input('Please input file number:'))]
    testing(readPath, writePath, readName)
    print('finish!!')
            
            
            
            
            
            