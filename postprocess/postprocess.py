""" 2016.8.20
刪除中研院parsing後結果與斷詞不符者
並取出正確者小樹部分
並處理原始資料刪除不符合者

2017.3.3
input 從 1991 改成 1991out.txt(標音結果)
    為了刪除標音去掉的部分
"""
name = input("please input the file name:")
file_read = "../data/input/%sseg_noPOS.txt" % name
file_read2 = "../data/input/%sout.txt" % name
file_write = "../data/postprocess/output/%sfullcts.txt" % name
file_write2 = "../data/postprocess/output/%sfaultcts.txt" % name
file_write3 = "../data/postprocess/output/%ssubcts.txt" % name
countline = 0
#找出非單字詞的行
with open(file_read , 'r') as fr:  # parsing結果
    lines = fr.readlines()
with open(file_read2 , 'r', encoding = 'utf8') as fr2:  # 標音結果
    lines2 = fr2.readlines()
    
lines2 = [lines2[4*i+2] for i in range(int(len(lines2)/4))]  # 只取句子

f1 = open(file_write, 'w', encoding = 'utf8')
f2 = open(file_write2, 'w', encoding = 'utf8')
f3 = open(file_write3, 'w', encoding = 'utf8')

for line2 in lines2:
    num = line2.split()[0]  # @num
    n = int(num.strip('@'))
    st = lines[n-1].split()[1]
    if st[0] == '%':
        f2.write(num + ' ')
        f2.write(st + '\n')
        continue
    countline = countline +1
    if ":行)" in st:
        f1.write(num + " ")
        f1.write(st + '\n')
        position = st.find(":行)")
        flag = 1      # 因為後面已經有一個括號
        # 尋找行)之後有幾個)
        for i in range(position, 0 ,-1):
            if st[i] == '(':
                flag -= 1
                if flag == 0:
                    newline = st[i:position+3]
                    break
            if st[i] == ')':
                flag += 1
        op = num + ' ' + newline + '\n'
        f3.write(op)
    elif ':行|' in st:
        # 印出被砍掉的部分且紀錄刪除的編號
        f1.write(num + " ")
        f1.write(st + '\n')
        position = st.find(":行|")
        flag = 1
        for i in range(position, len(st)):
            if st[i] == '(':
                flag += 1
            if st[i] == ')':
                flag -= 1
                if flag == 0:
                    st = st[0:i]
                    break          # 現在flag = 0
        for i in range(position, 0,-1):
            if st[i] == '(':
                flag -= 1
                if flag == -1:
                    newline = st[i:]
                    break
            if st[i] == ')':
                flag +=1
        op = num + ' ' + newline + ')\n'
        f3.write(op)

    else:
        f2.write(num + ' ')
        f2.write(st + '\n')
print("%ssubcts.txt ,%s.txt ,%sfulcts.txt & %sfaultcts.txt is made." % (name ,name ,name ,name))

