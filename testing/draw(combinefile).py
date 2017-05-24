# -*- coding: utf-8 -*-
"""
Created on Fri Apr  7 02:16:26 2017
畫圖
@author: speechlab

2017.4.15 更改幅度差距太大break y axis
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
plt.rcParams.update({'font.size': 13})

# get data from excel
readPath = '../data/combinefile/output'
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
cs2 = content[2]
cs3 = content[3]
ps1 = content[5]  # precision score1
ps2 = content[6]
ps3 = content[7]

ws1 = wb.get_sheet_by_name(sheets[1])
columns = ws1.columns

content = []
for row in columns:
    line = [col.value for col in row]
    content.append(line)

X = content[0]
c1s1 = content[1]  # correctRate score1
c1s2 = content[2]
c1s3 = content[3]
p1s1 = content[5]  # precision score1
p1s2 = content[6]
p1s3 = content[7]

# draw
def draw(s1, s2, s3, title):
    xticks = np.arange(len(X)) + 1
    allList = s1 + s2 + s3
    # set1:most data,   set2:far away from set1
    set1 = [i for i in allList if abs(i-(sum(allList)/len(allList)))<30]
    set2 = [i for i in allList if i not in set1]
    
    # just 1 group
    if not set2:
        ymin = math.floor(min(set1))
        ymax = math.ceil(max(set1))

        plt.figure(figsize=(20,15), dpi=120)
        plt.bar(xticks-0.25, s1, width = 0.25, facecolor='lightskyblue' ,edgecolor='white', label='score1', hatch='/')
        plt.bar(xticks, s2, width = 0.3, facecolor = 'yellowgreen',edgecolor = 'white', label='score2', hatch='o')
        plt.bar(xticks+0.25, s3, width = 0.25, facecolor = 'pink',edgecolor = 'white', label='score3', hatch='.')
        plt.xticks(xticks, X)
        plt.ylim(setRG(ymin-1),setRG(ymax+1))
        plt.xlabel('file')
        plt.ylabel('%')
        plt.title(title)
        plt.legend()
        for x,y in zip(xticks,s1):
            plt.text(x-0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s2):
            plt.text(x, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s3):
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
        ax.set_title(title)
        ax.bar(xticks-0.25, s1, width = 0.25, facecolor='lightskyblue' ,edgecolor='white', label='score1', hatch='/')
        ax.bar(xticks, s2, width = 0.3, facecolor = 'yellowgreen',edgecolor = 'white', label='score2', hatch='o')
        ax.bar(xticks+0.25, s3, width = 0.25, facecolor = 'pink',edgecolor = 'white', label='score3', hatch='.')
        ax.legend()
        ax2.bar(xticks-0.25, s1, width = 0.25, facecolor='lightskyblue' ,edgecolor='white', label='score1', hatch='/')
        ax2.bar(xticks, s2, width = 0.3, facecolor = 'yellowgreen',edgecolor = 'white', label='score2', hatch='o')
        ax2.bar(xticks+0.25, s3, width = 0.25, facecolor = 'pink',edgecolor = 'white', label='score3', hatch='.')
        for x,y in zip(xticks,s1):
            if y in set1:
                ax.text(x-0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
            else:
                ax2.text(x-0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s2):
            if y in set1:
                ax.text(x, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
            else:
                ax2.text(x, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
        for x,y in zip(xticks,s3):
            if y in set1:
                ax.text(x+0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')
            else:
                ax2.text(x+0.3, y+0.05, '%.1f' % y, ha='center', va= 'bottom')

        ax.set_ylim(setRG(ymin-1),setRG(ymax+1))
        ax2.set_ylim(setRG(ymin2-1),setRG(ymax2+1))
        plt.xticks(xticks, X)

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

draw(cs1, cs2, cs3, 'Correct Rate(all)')
draw(ps1, ps2, ps3, 'precision(all)')
draw(c1s1, c1s2, c1s3, 'Correct Rate(no_1)')
draw(p1s1, p1s2, p1s3, 'precision(no_1)')