# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 20:15:26 2017
def combilefile
@author: speechlab
"""
import score
from strprc import no_abc123

tone_ = ['do2', 'e3-sai4', 'ggau2', 'giann2', 'hang2', 'hing2', 'hing7', 'zua7']

def combinefile(lines1, lines2, r1, r2, _1List):
    spfault1 = []
    spfault2 = []
    score1 = [0,0,0,0]  # all(v, x) no1(v, x)
    score2= [0,0,0,0]
    score3 = [0,0,0,0]
    noFind = 0
    #temp = input('please input training file num:') 
    outputList = []  # initial
    amount1 = int(len(lines1)/7)  # amount of centence in lines1
    amount2 = int(len(lines2)/7)  # amount of centence in lines2
    if amount1 != amount2:
        print(amount1, ' / ', amount2)
        raise Exception('amount of sentence in file1 and 2 is inequality!')
    for i in range(amount1-1):
        # print('__', lines1[i*7+1])
        if lines1[i*7+1].split()[1][0] == '@':
            if lines1[i*7+1] == lines2[i*7+1]:  # two centence is equality
                outputList.append('\n')  # ' '
                outputList.append(lines1[i*7+1])  # '199x @oo'
                outputList.append(lines1[i*7+2])  # centence
                feature = f'{lines1[i*7+3][:-1]}{lines2[i*7+3]}'  # [(-1, 'T:之')][][]
                outputList.append(feature)
                tp = [item.split("'")[1] for item in feature.split(']') if len(item) >3]
                c1s1, tone1 = parse_scoreList(lines1[i*7+4])
                c2s1, tone2 = parse_scoreList(lines2[i*7+4])
                s1List = add(c1s1, c2s1, r1, r2)
                c1s2, tone1 = parse_scoreList(lines1[i*7+5])
                c2s2, tone2 = parse_scoreList(lines2[i*7+5])
                s2List = add(c1s2, c2s2, r1, r2)
                c1s3, tone1 = parse_scoreList(lines1[i*7+6])
                c2s3, tone2 = parse_scoreList(lines2[i*7+6])
                s3List = add(c1s3, c2s3, r1, r2)
                s1 = score.Score(s1List, tone1)
                if isinstance(s1List, list):
                    situation1 = s1.judge(tp, _1List)  # all(v,x) + no1(v,x) + spError(1,2)
                    score1 = [a+b for a, b in zip(situation1[:4], score1)]
                    if situation1[4] == 1:  # 特殊錯誤1
                        spfault1.append('s1 '+lines1[i*7+1][:-1]+s1.tone.ljust(8)+s1.predictone.ljust(8)+str(feature).ljust(30) + '\n')
                    if situation1[5] == 1:  # 特殊錯誤2
                        spfault2.append('s1 '+lines1[i*7+1][:-1]+s1.tone.ljust(8)+s1.predictone.ljust(8)+str(feature).ljust(30) + '\n')
                    outputList.append(str(s1List).ljust(50) + tone1.ljust(8) + 
                                  f'{s1.rank}/{s1.allrank}\n')
                else:
                    noFind = noFind + 1 
                    outputList.append('noFind'.ljust(50) + tone1.ljust(8))
                s2 = score.Score(s2List, tone1)
                if isinstance(s2List, list):
                    situation2 = s2.judge(tp, _1List)  # all(v,x) + no1(v,x) + spError(1,2)
                    score2 = [a+b for a, b in zip(situation2[:4], score2)]
                    if situation2[4] == 1:  # 特殊錯誤1
                        spfault1.append('s2 '+lines1[i*7+1][:-1]+s2.tone.ljust(8)+s2.predictone.ljust(8)+str(feature).ljust(30) + '\n')
                    if situation2[5] == 1:  # 特殊錯誤2
                        spfault2.append('s2 '+lines1[i*7+1][:-1]+s2.tone.ljust(8)+s2.predictone.ljust(8)+str(feature).ljust(30) + '\n')
                    outputList.append(str(s2List).ljust(50) + tone1.ljust(8) + 
                                  f'{s2.rank}/{s2.allrank}\n')
                else:
                    noFind = noFind + 1 
                    outputList.append('noFind'.ljust(50) + tone1.ljust(8))
                s3 = score.Score(s3List, tone1)
                if isinstance(s3List, list):
                    situation3 = s3.judge(tp, _1List)  # all(v,x) + no1(v,x) + spError(1,2)
                    score3 = [a+b for a, b in zip(situation3[:4], score3)]
                    if situation3[4] == 1:  # 特殊錯誤1
                        spfault1.append('s3 '+lines1[i*7+1][:-1]+s3.tone.ljust(8)+s3.predictone.ljust(8)+str(feature).ljust(30) + '\n')
                    if situation3[5] == 1:  # 特殊錯誤2
                        spfault2.append('s3 '+lines1[i*7+1][:-1]+s3.tone.ljust(8)+s3.predictone.ljust(8)+str(feature).ljust(30) + '\n')
                    outputList.append(str(s3List).ljust(50) + tone1.ljust(8) + 
                                  f'{s3.rank}/{s3.allrank}\n')
                else:
                    noFind = noFind + 1 
                    outputList.append('noFind'.ljust(50) + tone1.ljust(8))
                

    correctRate = [format(round(score[0]/(score[0]+score[1]),5)*100, '.3f') for score in (score1, score2, score3)]  # 一次有算 
    prec = [format(round(score[0]/(score[0]+score[1]+noFind),5)*100, '.3f') for score in (score1, score2, score3)]
    correctRate1 = [format(round(score[2]/(score[2]+score[3]),5)*100, '.3f') for score in (score1, score2, score3)]  # 一次不算
    prec1 = [format(round(score[2]/(score[2]+score[3]+noFind),5)*100, '.3f') for score in (score1, score2, score3)]
                
    outputList.append(f'\n\n共{amount1}, 找不到特徵詞:{noFind}\n\n')
    outputList.append(f'S1 正確:{score1[0]}, 錯誤:{score1[1]}, 正確率={correctRate[0]}% precision:{prec[0]}%\n')
    outputList.append(f'不算詞頻為1的特徵詞 正確:{score1[2]} 錯誤:{score1[3]} 正確率:{correctRate1[0]}% precision:{prec1[0]}%\n\n')
    outputList.append(f'S2 正確:{score2[0]}, 錯誤:{score2[1]}, 正確率={correctRate[1]}% precision:{prec[1]}%\n')
    outputList.append(f'不算詞頻為1的特徵詞 正確:{score2[2]} 錯誤:{score2[3]} 正確率:{correctRate1[1]}% precision:{prec1[1]}%\n\n')
    outputList.append(f'S3 正確:{score3[0]}, 錯誤:{score3[1]}, 正確率={correctRate[2]}% precision:{prec[2]}%\n')
    outputList.append(f'不算詞頻為1的特徵詞 正確:{score3[2]} 錯誤:{score3[3]} 正確率:{correctRate1[2]}% precision:{prec1[2]}%\n\n')
    return outputList, spfault1, spfault2, correctRate, prec, correctRate1, prec1
                
                
                
                
        
# 從string獲得score and tone        
def parse_scoreList(string):
    if string.split()[0] == 'no':
        tone = string.split()[2]
        return [0, 0, 0, 0, 0, 0, 0, 0], tone
    elif string.split()[0] == 'inapplicable'
        tone = string.split()[2]
        return [0, 0, 0, 0, 0, 0, 0, 0], tone
    else:
        score = string.split('[')[1].split(']')[0].split(', ')
        score = [float(item) for item in score]
        tone = string.split('] ')[1].split()[0]  # correct ans
        return score, tone

# 分數相加
def add(c1, c2, r1, r2):
    try:
        return [round(a*r1+b*r2, 2) for a, b in zip(c1, c2)]
    except TypeError:
        if isinstance(c1, list):
            return c1
        elif isinstance(c2, list):
            return c2
        else:
            return 'noFind'