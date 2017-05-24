'''2017.3.26
寫成class

2017.4.11
replace '行' ==> '*' 只改第一個
'''

from nltk.tree import Tree


class Grab:
    def __init__(self, str):
        self.string = str
        self.string = self.string.replace(':行)', ':*)', 1)
        self.string = self.string.replace(':行|', ':*|', 1)  # 辨別單字詞行
        self.string = self.string.replace('‧的', '')  # 拿掉‧的
        self.string = self.string.replace('‧地', '')  # 拿掉‧地
        self.string = self.string.split('#')[0]  # 拿掉標點符號
    # 取得所有head    
    def all_head(self, *posi):
        str = self.string
        str = str.replace('(', '|')
        str = str.replace(')', '')
        items = str.split('|')
        items = [item for item in items if item != '']  # 移除空白項
        items = [item for item in items if is_chinese(item[-1]) is True]  # 確保該項是詞不是語意角色
        tempList = [i for i in items if 'Head'in i or '*' in i]
        for n, item in enumerate(tempList):
            if item.find('*') != -1:
                po = n
                break
        if posi:
            newList = [(n-po, i) for n, i in enumerate(tempList) if n-po in posi]
        else:
            newList = [(n-po, i) for n, i in enumerate(tempList)]
        return newList
    # 取得整句中與行距離為n以內的所有詞
    def nb(self, *posi):
        str = self.string
        str = str.replace(')', '')
        str = str.replace('(', '|')
        items = str.split('|')
        items = [item for item in items if item != '']  # 移除空白項
        items = [item for item in items if is_chinese(item[-1]) is True]
        for n, item in enumerate(items):
            if item.find('*') != -1:
                po = n
                break
        if posi:
            newList = [(n-po, i) for n, i in enumerate(items) if n-po in posi]
        else:    
            newList = [(n-po, i) for n, i in enumerate(items)]
        return newList
    # 取出樹中'行'的鄰居
    def tree_nb(self, layerNum=0, *posi):
        str = self.string
        if layerNum == 0:
            items = dependence(str)
        elif layerNum > 0:
            items = dpds(str, layerNum)
        else:
            raise Exception("Layer number must be greater than 0")
        
        
        for n, item in enumerate(items):
            if item.find('*') != -1:
                po = n
                break
        if posi:
            try:
                newList = [(n-po, i) for n, i in enumerate(items) if n-po in posi]
            except:
                newList = []
        else:    
            try:
                newList = [(n-po, i) for n, i in enumerate(items)]
            except:
                newList = []
                print('_______________', items)
                print(str)
        return newList
    

# 判斷中文
def is_chinese(text):
    return all(('\u4e00' <= char <= '\u9fff' or char in ['*', '、']) for char in text)

# 作str 的tree
def tree(str):
    str = str.replace('head:', 'head-')
    str = str.replace('Head:', 'Head-')
    str = str.replace(':', ' ')
    str = str.replace('|', ') (')
    str = str.replace('-', ':')
    str = '(' + str + ')'
    return Tree.fromstring(str)

# 找到代表該NODE的Head的升上來的詞
def find_up(tree):
    tempList = []  # 暫存目標
    if len(tree) == 1:  #  只有一分支
        if isinstance(tree[0], str):
            return [f'{tree.label()}:{tree[0]}']
        else:
            try:
                return find_up(tree[0])
            except:
                test = tree[0]
                print(test)
    else:
        for subtree in tree:
            label = subtree.label()
            if 'Head' in label:
                if isinstance(subtree[0], str):
                    tempList.append(f'{label}:{subtree[0]}')
                else:
                    return find_up(subtree)
        if not tempList:  # 如果沒找到Head
            for subtree in tree:
                if 'head' in subtree.label():
                    return find_up(subtree)
        else:  # 有找到Head
            return tempList
            
                
              
# 找鄰居
def find_nb_in_tree(tree):
    nblist = []
    for subtree in tree:
        if isinstance(subtree[0], str) and len(subtree) == 1:
            nblist.append(f'{subtree.label()}:{subtree[0]}')
        else:
            temp = find_up(subtree)
            if temp:
                nblist = nblist + temp
    return nblist        

# 找第N層鄰居
def dpds(str, n):
    t = tree(str)
    leafnum = t.leaves().index('*')
    p = t.leaf_treeposition(leafnum)  # tuple
    if n == 1:
        ans = find_nb_in_tree(t[p[:-2]])
    else:
        if 'Head' not in t[p[:-n]].label():
            return []
        else:
            ans = find_nb_in_tree(t[p[:-(n+1)]])
        
    str = str.replace(')', '')
    str = str.replace('(', '|')
    items = str.split('|')
    items = [item for item in items if item != '']  # 移除空白項
    items = [item for item in items if is_chinese(item[-1]) is True]
    tempList = [i for i in items if i in ans]
    return tempList

                    
# 找出與'行'相依的詞
def dependence(str):
    t = tree(str)
    leafnum = t.leaves().index('*')
    p = t.leaf_treeposition(leafnum)  # tuple
    for n in range(1, len(p)):
        if n == 1:
            ans = find_nb_in_tree(t[p[:-2]])
        else:
            if 'Head' in t[p[:-n]].label():
                ans = ans + find_nb_in_tree(t[p[:-(n+1)]])
    
       
    str = str.replace(')', '')
    str = str.replace('(', '|')
    items = str.split('|')
    items = [item for item in items if item != '']  # 移除空白項
    items = [item for item in items if is_chinese(item[-1]) is True]
    tempList = [i for i in items if i in ans]
    return tempList
         

# main function
if __name__ == '__main__':
    
    import glob
    fw = open('test.txt', 'w', encoding='utf8')
    path = '../find2head/*fullcts.txt'
    fileList = glob.glob(path)
    for n,file in enumerate(fileList):
        with open(file, 'r', encoding = 'utf8') as f:
            lines = f.readlines()
        
        for line in lines:
            num = line.split()[0]
            st = line.split()[1]
            out = Grab(st)
            
            fw.write(f'{num}  {out.tree_nb(2)}')
            fw.write('    '+st+'\n')
    fw.close()



