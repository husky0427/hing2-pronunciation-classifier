# -*- coding: utf-8 -*-
"""2017.3.15

@author: husky0427
2017.3.28 隨grab修改更新

2017.4.5 改成def
"""
import os
import math
import syndict
import grab4 as grab
import score as scorecalcu
from strprc import no_abc123, no_chinese

# global variable
start = 0  # 檔案開始
end = 5  # 檔案結束
dictswitch = 1  # synDict Switch

tone_ = ['do2', 'e3-sai4', 'ggau2', 'giann2', 'hang2', 'hing2', 'hing7', 'zua7']
trainNum = ['1991', '1992', '1993', '1994', '1995', '1996', '1997']

def testing_combined(readPath, writePath, readName1, readName2, r1, r2):
    
    # user input
    trainingDict1 = {}
    trainingDict2 = {}
    _1List = []  # 只出現一次的詞
    cnt = 0
    v = [0, 0, 0]  # 正確
    x = [0, 0, 0]  # 錯誤
    noFind = 0
    v1 = [0, 0, 0]  # (不計入training只有一次的) 
    x1 = [0, 0, 0]
    inappli = 0



    ctsMethod = readName1[:-10].split('_')[1]
    grabMethod = readName1[:-10].split('_')[0].split('(')[0]
    posi1 = [int(readName1[:-10].split('_')[2])]
    posi2 = [int(readName2[:-10].split('_')[2])]

    writeName = f'combine_{posi1}_{posi2}_{r1}-{r2}.txt'
    writeNameRp1 = writeName[:-4] + '(testRp1).txt'
    writeNameRp2 = writeName[:-4] + '(testRp2).txt'

    # loading training data
    with open(os.path.join(readPath, readName1), 'r') as fr:
        words = fr.readlines()
    for word in words:
        index = word.split()[0]
        freq = int(word.split()[1])
        score = word.split('[')[1].split(']')[0]
        score = score.split(', ')
        scoreList1 = [round(int(n)/freq,2) for n in score]  # 比例
        scoreList2 = [int(n) for n in score]  # 次數
        scoreList3 = [round(math.log2(1+n), 2) for n in scoreList2]  # 次數log
        trainingDict1[index] = scoreList1, scoreList2, scoreList3
        if freq == 1:
            _1List.append(index)

    with open(os.path.join(readPath, readName2), 'r') as fr:
        words = fr.readlines()
    for word in words:
        index = word.split()[0]
        freq = int(word.split()[1])
        score = word.split('[')[1].split(']')[0]
        score = score.split(', ')
        scoreList1 = [round(int(n)/freq,2) for n in score]  # 比例
        scoreList2 = [int(n) for n in score]  # 次數
        scoreList3 = [round(math.log2(1+n), 2) for n in scoreList2]  # 次數log
        trainingDict2[index] = scoreList1, scoreList2, scoreList3
        if freq == 1:
            _1List.append(index)        
    
    # syndict
    syn1 = syndict.syn_dict(trainingDict1)
    syn2 = syndict.syn_dict(trainingDict2)

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
                feature1 = content.nb(*posi1)
            elif grabMethod == 'allhead':
                feature1 = content.all_head(*posi1)
            elif grabMethod == 'treenb':
                layerNum = readName1.split('(')[1].split(')')[0]
                feature1 =  content.tree_nb(int(layerNum), *posi1)
            if grabMethod == 'nb':
                feature2 = content.nb(*posi2)
            elif grabMethod == 'allhead':
                feature2 = content.all_head(*posi2)
            elif grabMethod == 'treenb':
                layerNum = readName2.split('(')[1].split(')')[0]
                feature2 =  content.tree_nb(int(layerNum), *posi2)  

            # 若該方法沒有特徵詞    
            if feature1 == [] and feature2 == []:  
                noFind += 1
                fw.write('[][]\n')
                fw.write('no feature'.ljust(50)+ tone + '\n')  # 正確讀音)
                fw.write('no feature'.ljust(50)+ tone + '\n')  # 正確讀音)
                fw.write('no feature'.ljust(50)+ tone + '\n')  # 正確讀音)
            else:
                fw.write(f'{feature1}{feature2}\n')
                for tp in feature1:  # tuple:(1, 'DET:一')7
                    ch = no_abc123(tp[1])
                    p = tp[0]
                    try:
                        sc1 = syn1.get_score(ch, scoreNum=1, dictSwitch=dictswitch)
                        t_score1 = [round(r1/(r1+r2)*a+b,2) for a,b in zip(sc1, t_score1)]
                        sc2 = syn1.get_score(ch, scoreNum=2, dictSwitch=dictswitch)
                        t_score2 = [round(r1/(r1+r2)*a+b,2) for a,b in zip(sc2, t_score2)]
                        sc3 = syn1.get_score(ch, scoreNum=3, dictSwitch=dictswitch)
                        t_score3 = [round(r1/(r1+r2)*a+b,2) for a,b in zip(sc3, t_score3)]
                    except KeyError:
                        pass
                for tp in feature2:  # tuple:(1, 'DET:一')7
                    ch = no_abc123(tp[1])
                    p = tp[0]
                    try:   
                        sc1 = syn2.get_score(ch, scoreNum=1, dictSwitch=dictswitch)
                        t_score1 = [round(r2/(r1+r2)*a+b,2) for a,b in zip(sc1, t_score1)]
                        sc2 = syn2.get_score(ch, scoreNum=2, dictSwitch=dictswitch)
                        t_score2 = [round(r2/(r1+r2)*a+b,2) for a,b in zip(sc2, t_score2)]
                        sc3 = syn2.get_score(ch, scoreNum=3, dictSwitch=dictswitch)
                        t_score3 = [round(r2/(r1+r2)*a+b,2) for a,b in zip(sc3, t_score3)]
                    except KeyError:
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
                correctList = s1.judge(feature1+feature2, _1List)
                v[0] = v[0] + s1.correctList1[0]
                x[0] = x[0] + s1.correctList1[1]
                v1[0] = v1[0] + s1.correctList2[0]
                x1[0] = x1[0] + s1.correctList2[1]
                if s1.spFault[0] == 1:
                    fw_report1.write('s1 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report1.write(tone.ljust(8)+s1.predictone.ljust(8))  # 第一種錯誤紀錄
                    fw_report1.write(str(feature1+feature2)+'\n')
                if s1.spFault[1] == 1:
                    fw_report2.write('s1 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report2.write(tone.ljust(8)+s1.predictone.ljust(8))  # 第二種錯誤紀錄
                    fw_report2.write(str(feature1+feature2)+ '\n')                
                fw.write(str(t_score1).ljust(50) + tone.ljust(8) + str(s1.rank) + '/'
                     + str(s1.allrank) + '\n')
                # 分數2
                s2 = scorecalcu.Score(t_score2, tone)
                correctList = s2.judge(feature1+feature2, _1List)
                v[1] = v[1] + s2.correctList1[0]
                x[1] = x[1] + s2.correctList1[1]
                v1[1] = v1[1] + s2.correctList2[0]
                x1[1] = x1[1] + s2.correctList2[1]
                if s2.spFault[0] == 1:
                    fw_report1.write('s2 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report1.write(tone.ljust(8)+s2.predictone.ljust(8))  # 第一種錯誤紀錄
                    fw_report1.write(str(feature1+feature2)+ '\n')
                if s2.spFault[1] == 1:
                    fw_report2.write('s2 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report2.write(tone.ljust(8)+s2.predictone.ljust(8))  # 第二種錯誤紀錄
                    fw_report2.write(str(feature1+feature2)+ '\n')                
                fw.write(str(t_score2).ljust(50) + tone.ljust(8) + str(s2.rank) + '/'
                     + str(s2.allrank) + '\n')
                # 分數3
                s3 = scorecalcu.Score(t_score3, tone)
                correctList = s3.judge(feature1+feature2, _1List)
                v[2] = v[2] + s3.correctList1[0]
                x[2] = x[2] + s3.correctList1[1]
                v1[2] = v1[2] + s3.correctList2[0]
                x1[2] = x1[2] + s3.correctList2[1]
                if s3.spFault[0] == 1:
                    fw_report1.write('s3 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report1.write(tone.ljust(8)+s3.predictone.ljust(8))  # 第一種錯誤紀錄
                    fw_report1.write(str(feature1+feature2)+ '\n')
                if s3.spFault[1] == 1:
                    fw_report2.write('s3 '+fileNum.ljust(7)+num.ljust(7))
                    fw_report2.write(tone.ljust(8)+s3.predictone.ljust(8))  # 第二種錯誤紀錄
                    fw_report2.write(str(feature1+feature2)+ '\n')                
                fw.write(str(t_score3).ljust(50) + tone.ljust(8) + str(s3.rank) + '/'
                     + str(s3.allrank) + '\n')
    
    prec = [format(round(t/(t+f),5)*100, '.3f') for t, f in zip(v, x)]  # 一次有算 
    prec1 = [format(round(t/(t+f),5)*100, '.3f') for t, f in zip(v1, x1)]  # 一次不算
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
    print('finish') 
    return cnt, noFind, inappli, applicRate, prec, prec1
             
            
            
            

            
            
            
            
            