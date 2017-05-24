# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 02:16:26 2017
畫圖 for combine
@author: speechlab
"""
import os
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
from openpyxl import load_workbook

#set range = 1~100
def setRG(num):
    if num > 100:
        return 100
    elif num < 0:
        return 0
    else:
        return num

# change font size
plt.rcParams.update({'font.size': 22})

# get data from excel
readPath = '../data/testing/output'
fileList = glob.glob(f'{readPath}/*.xlsx')
readName = os.path.split(fileList[0])[1]
print(fileList)

wb = load_workbook(filename=fileList[0])
sheets = wb.get_sheet_names()
ws = wb.get_sheet_by_name(sheets[0])
columns = ws.columns

content = []
for row in columns:
    line = [col.value for col in row]
    content.append(line)

X = content[0]
cs1 = content[1]  # correctRate score1
ps1 = content[2]  # precision score1


ws1 = wb.get_sheet_by_name(sheets[1])
columns = ws1.columns

content = []
for row in columns:
    line = [col.value for col in row]
    content.append(line)
    
X = content[0]
c1s1 = content[1]  # correctRate score1
p1s1 = content[2]  # precision score1

# draw
def draw(s1, s2, s3, s4, title):
    xticks = np.arange(len(X)) + 1
    allList = s1 + s2 + s3 + s4
    # set1:most data,   set2:far away from set1
    mean = sum(allList) / len(allList)
    var = sum([(d - mean)**2 for d in allList]) / len(allList)
    if var > 1000:
        set1 = [i for i in allList if i > mean]
    else:
        set1 = allList
    set2 = [i for i in allList if i not in set1]
    # just 1 group
    if not set2:
        ymin = math.floor(min(set1))
        ymax = math.ceil(max(set1))
        plt.figure(figsize=(28,21), dpi=120)
        plt.bar(xticks-0.3, s1, width = 0.2, facecolor='lightskyblue' ,edgecolor='white', label='CR', hatch='/')
        plt.bar(xticks-0.1, s2, width = 0.2, facecolor='yellowgreen' ,edgecolor='white', label='PR', hatch='o')
        plt.bar(xticks+0.1, s3, width = 0.2, facecolor='pink' ,edgecolor='white', label='CR(no 1)', hatch='.')
        plt.bar(xticks+0.3, s4, width = 0.2, facecolor='purple' ,edgecolor='white', label='PR(no 1)', hatch='+')
        plt.xticks(xticks, X)
        plt.ylim(setRG(ymin-1),setRG(ymax+1))
        plt.xlabel('file')
        plt.ylabel('%')
        plt.title(title)
        plt.legend()
        for x,y in zip(xticks,s1):
            plt.text(x-0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s2):
            plt.text(x-0.1, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s3):
            plt.text(x+0.1, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s4):
            plt.text(x+0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')        
        plt.savefig(f'{readPath}/{title}.png', dpi=120)
    # 2group
    else:
        if sum(set2)/len(set2) > sum(set1)/len(set1):  # averagy set2 > set1
            set1, set2 = set2, set1
        ymin = math.floor(min(set1))  # ax1
        ymax = math.ceil(max(set1))
        ymin2 = math.floor(min(set2))  # ax2
        ymax2 = math.ceil(max(set2))
        f, (ax, ax2) = plt.subplots(2, 1, sharex=True, figsize=(20,15), dpi=120)
        plt.xlabel('file')
        plt.ylabel('%')
        ax.set_ylim(setRG(ymin-1),setRG(ymax+1))
        ax.set_title(title)
        ax.bar(xticks-0.3, s1, width = 0.2, facecolor='lightskyblue' ,edgecolor='white', label='CR', hatch='/')
        ax.bar(xticks-0.1, s2, width = 0.2, facecolor='yellowgreen' ,edgecolor='white', label='PR', hatch='o')
        ax.bar(xticks+0.1, s3, width = 0.2, facecolor='pink' ,edgecolor='white', label='CR(no 1)', hatch='.')
        ax.bar(xticks+0.3, s4, width = 0.2, facecolor='purple' ,edgecolor='white', label='PR(no 1)', hatch='+')
        print('y2=', ymin2, ymax2)
        ax2.set_ylim(setRG(ymin2-1),setRG(ymax2+1))
        ax2.bar(xticks-0.3, s1, width = 0.2, facecolor='lightskyblue' ,edgecolor='white', label='CR', hatch='/')
        ax2.bar(xticks-0.1, s2, width = 0.2, facecolor='yellowgreen' ,edgecolor='white', label='PR', hatch='o')
        ax2.bar(xticks+0.1, s3, width = 0.2, facecolor='pink' ,edgecolor='white', label='CR(no 1)', hatch='.')
        ax2.bar(xticks+0.3, s4, width = 0.2, facecolor='purple' ,edgecolor='white', label='PR(no 1)', hatch='+')
        ax.legend()
        for x,y in zip(xticks,s1):
            if y in set1:
                ax.text(x-0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
            else:
                ax2.text(x-0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s2):
            if y in set1:
                ax.text(x-0.1, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
            else:
                ax2.text(x-0.1, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s3):
            if y in set1:
                ax.text(x+0.1, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
            else:
                ax2.text(x+0.1, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s4):
            if y in set1:
                ax.text(x+0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
            else:
                ax2.text(x+0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        
        ax.spines['bottom'].set_visible(False)
        ax2.spines['top'].set_visible(False)
        d = 0.015  # how big to make the diagonal lines in axes coordinates
        kwargs = dict(transform=ax.transAxes, color='k', clip_on=False)
        ax.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
        ax.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal
        kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
        ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
        ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal
    
        plt.savefig(f'{readPath}/{title}.png', dpi=120)
        
draw(cs1, ps1, c1s1, p1s1, readName.split('.')[0])
