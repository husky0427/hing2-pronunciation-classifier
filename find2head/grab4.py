'''2017.3.26
寫成class

'''

from nltk.tree import Tree


class Grab:
    def __init__(self, str):
        self.string = str
        self.string = self.string.replace(':行)', ':*)')
        self.string = self.string.replace(':行|', ':*|')  # 辨別單字詞行
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
            newList = [(n-po, i) for n, i in enumerate(items) if n-po in posi]
        else:    
            try:
                newList = [(n-po, i) for n, i in enumerate(items)]
            except:
                newList = []
        return newList
    

# 判斷中文
def is_chinese(text):
    return all(('\u4e00' <= char <= '\u9fff' or char == '*') for char in text)

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
    for subtree in tree:
        try:  # 避免底層str沒有label()
            label = subtree.label()
        except:
            label = subtree
        if 'Head' in label:
            try:
                return label + ':' + subtree[0]
                break
            except:
                return find_up(subtree)
    else:
        for subtree in tree:
            if 'head' in subtree:
                return find_up(subtree)
            break
        else:
            for subtree in tree:
                return find_up(subtree)
                
              
# 找鄰居
def find_nb_in_tree(tree):
    nblist = []
    for subtree in tree:
        if len(subtree) == 1:
            try:
                nblist.append(subtree.label() + ':' + subtree[0])
            except:
                nblist.append(subtree[0].label() + ':' + subtree[0][0])
        else:
            temp = find_up(subtree)
            if temp:
                nblist.append(temp)
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
    with open('../data/grablist/input/1991fullcts.txt', 'r', encoding = 'utf8') as f:
        lines = f.readlines()
        
    for line in lines:
        num = line.split()[0]
        st = line.split()[1]
        out = Grab(st)
        print(num, '  ', out.tree_nb(), '\n')
        print(st, '\n\n')

