# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 09:00:37 2017
function of combine
@author: speechlab
"""
import score
from strprc import no_abc123
import os

def combinefiles(fileDatas, CoefTupleOfData):  # fileDatas is a list
    
    output_text = []  # texts of output
    spfault1 = []
    spfault2 = []
    v = [0, 0, 0]
    x = [0, 0, 0]
    noFind = 0
    inappli = 0
    
    def check_num_of_coef(fileDatas, CoefTupleOfData):
        if len(CoefTupleOfData) != len(fileDatas):
            raise TypeError('''Numbers of coefficients are not equal 
                            to number of file datas!''')
    # check lines numbers of file datas are equal
    def check_lineno(fileData):
        if len({len(fileData) for fileData in fileDatas}) > 1:
            raise TypeError('''amount of sentence in file1 and 2 is 
                            inequality!''')
    # 從string獲得score and tone        
    def str2int_scoreList(string):
        if string.split()[0] == 'no':
            tone = string.split()[2]
            return [0, 0, 0, 0, 0, 0, 0, 0], tone
        elif string.split()[0] == 'inapplicable':
            tone = string.split()[1]
            return [0, 0, 0, 0, 0, 0, 0, 0], tone
        else:
            score = string.split('[')[1].split(']')[0].split(', ')
            score = [float(item) for item in score]
            tone = string.split('] ')[1].split()[0]  # correct ans
            return score, tone
    
    def sum_of_score(scoreList):
        sumList = [0, 0, 0, 0, 0, 0, 0, 0]
        for sc, r in zip(scoreList, CoefTupleOfData):
            temp = [n*r for n in sc]
            sumList = [a + b for a, b in zip(temp, sumList)]
        sumList = [round(s/sum(CoefTupleOfData), 2) for s in sumList]
        return sumList
    
    check_num_of_coef(fileDatas, CoefTupleOfData)
    check_lineno(fileDatas)
    amountOfLines = int(len(fileDatas[0])/7)
    dataSample = fileDatas[0]  # set data 1 as data sample
    
    
    for i in range(amountOfLines-1):
        if dataSample[i*7+1].split()[1][0] != '@':
            raise Exception('data start from not "@"!')
        
        output_text.append('\n')  # ' '
        output_text.append(dataSample[i*7+1])  # '199x @oo'
        output_text.append(dataSample[i*7+2])  # centence
        # feature
        feature = ''
        for fileData in fileDatas:
            feature = feature.join(fileData[i*7+3][:-1])
        feature += '\n'
        output_text.append(feature)
                    
        # score
        s1List = []  # load s1 of datas
        s2List = []  # load s2 of datas
        s3List = []  # load s3 of datas       
        for fileData in fileDatas:
            tempScore, tone = str2int_scoreList(fileData[i*7+4])
            s1List.append(tempScore)
            tempScore, tone = str2int_scoreList(fileData[i*7+5])
            s2List.append(tempScore)
            tempScore, tone = str2int_scoreList(fileData[i*7+6])
            s3List.append(tempScore)
        
        # judgment of no feature
        if no_abc123(feature) == '':
            noFind += 1
            output_text.append('no feature'.ljust(50) + tone.ljust(8) + '\n')
            output_text.append('no feature'.ljust(50) + tone.ljust(8) + '\n')
            output_text.append('no feature'.ljust(50) + tone.ljust(8) + '\n')
            continue
        
        sum1 = sum_of_score(s1List)
        sum2 = sum_of_score(s2List)
        sum3 = sum_of_score(s3List)
        
        # judgment of inapplibility
        if sum2 == [0, 0, 0, 0, 0, 0, 0, 0]:
            inappli += 1
            output_text.append('inapplicable'.ljust(50) + tone + '\n')
            output_text.append('inapplicable'.ljust(50) + tone + '\n')
            output_text.append('inapplicable'.ljust(50) + tone + '\n')
            continue
        
        s1 = score.Score(sum1, tone)
        s2 = score.Score(sum2, tone)
        s3 = score.Score(sum3, tone)
        v[0] = s1.judge2()[0] + v[0]
        v[1] = s2.judge2()[0] + v[1]
        v[2] = s3.judge2()[0] + v[2]
        x[0] = s1.judge2()[1] + x[0]
        x[1] = s2.judge2()[1] + x[1]
        x[2] = s3.judge2()[1] + x[2]
        if s1.judge2()[2] == 1:  # 特殊錯誤1
            spfault1.append('s1 '+ dataSample[i*7+1][:-1]+s1.tone.ljust(8)+s1.predictone.ljust(8)+str(feature).ljust(30) + '\n')
        if s1.judge2()[3] == 1:  # 特殊錯誤2
            spfault2.append('s1 '+ dataSample[i*7+1][:-1]+s1.tone.ljust(8)+s1.predictone.ljust(8)+str(feature).ljust(30) + '\n')
        if s2.judge2()[2] == 1:  # 特殊錯誤1
            spfault1.append('s2 '+ dataSample[i*7+1][:-1]+s2.tone.ljust(8)+s2.predictone.ljust(8)+str(feature).ljust(30) + '\n')
        if s2.judge2()[3] == 1:  # 特殊錯誤2
            spfault2.append('s2 '+ dataSample[i*7+1][:-1]+s2.tone.ljust(8)+s2.predictone.ljust(8)+str(feature).ljust(30) + '\n')
        if s3.judge2()[2] == 1:  # 特殊錯誤1
            spfault1.append('s2 '+ dataSample[i*7+1][:-1]+s3.tone.ljust(8)+s3.predictone.ljust(8)+str(feature).ljust(30) + '\n')
        if s3.judge2()[3] == 1:  # 特殊錯誤2
            spfault2.append('s2 '+ dataSample[i*7+1][:-1]+s3.tone.ljust(8)+s3.predictone.ljust(8)+str(feature).ljust(30) + '\n')
        # output
        output_text.append(str(s1.score).ljust(50) + tone.ljust(8) + f'{s1.rank}/{s1.allrank}\n')
        output_text.append(str(s2.score).ljust(50) + tone.ljust(8) + f'{s2.rank}/{s2.allrank}\n')
        output_text.append(str(s3.score).ljust(50) + tone.ljust(8) + f'{s3.rank}/{s3.allrank}\n')
        
    cnt = amountOfLines - 1
    try:
        prec = [format(round(t/(t+f),5)*100, '.3f') for t, f in zip(v, x)]  # 一次有算 
    except ZeroDivisionError:
        prec = [0,0,0]
    applicRate = format(round((cnt-noFind-inappli)/cnt,5)*100, '.3f')    
    
    output_text.append(f'\n\n共{cnt}句, no feature:{noFind}, inapplicable:{inappli}, applicability:{applicRate}%\n')
    output_text.append(f'\nS1 正確:{v[0]}, 錯誤:{x[0]}, precision:{prec[0]}%\n')
    output_text.append('')
    output_text.append(f'\nS2 正確:{v[1]}, 錯誤:{x[1]}, precision:{prec[1]}%\n')
    output_text.append('') 
    output_text.append(f'\nS3 正確:{v[2]}, 錯誤:{x[2]}, precision:{prec[2]}%\n')
    output_text.append('')
    
    print('finish!!')
    return cnt, noFind, inappli, applicRate, prec, output_text, spfault1, spfault2
        
        
if __name__=="__main__":  
    readPath = '../data/combinefile/input'
    writePath = '../data/combinefile/output'
    writeName = 'cb'
    for n, i in enumerate(os.listdir(readPath)):
        print(n, ' ', i)
    # read multiple file
    readNameList = []
    ratioList = []
    index = 1
    keyin = ''
    while 1:
        for i, name in enumerate(readNameList):
            print(i, ' ', name)
        try:
            keyin = int(input(f'Please input file{index} number:'))
        except:  # keyin == 'x'
            break
        ratio = float(input(f'Please input file{index} ratio:'))
        ratioList.append(ratio)
        readNameList.append(os.listdir(readPath)[keyin])
        index += 1
        # 
        
    textList = []
    for name in readNameList:
        with open(f'{readPath}/{name}', encoding='utf8') as fr:
            textList.append(fr.readlines())
            
    # combine 2 files
    temp = combinefiles(textList, ratioList)
    cnt = temp[0]
    noFind = temp[1]
    inappli = temp[2]
    applicRate = temp[3]
    prec = temp[4]
    text = temp[5]
    spfault1 = temp[6]
    spfault2 = temp[7]
    
    with open(f'{writePath}/{writeName}(test).txt', 'w', encoding='utf8') as fw:
        for line in text:
            fw.write(line)
    
    with open(f'{writePath}/{writeName}(RP1).txt', 'w', encoding='utf8') as fw2:
        for line in spfault1:
            fw2.write(line)
            
    with open(f'{writePath}/{writeName}(RP2).txt', 'w', encoding='utf8') as fw3:
        for line in spfault2:
            fw3.write(line)
        
        