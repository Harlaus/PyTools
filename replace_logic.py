#-*-coding:utf-8-*-
import re

#覆盖所有字段
#text    旧字符串
#char    关键字
#new_char新关键字
def replace_all(text='',char='',new_char=''):
    return text.replace(char,new_char)

#覆盖一行
#text     旧字符串
#char     关键字
#new_char 新关键字
#auto_add 自动填充自增数
#change_char 指代自增数
def replace_one_by_one(text='',char='',new_char='',auto_add=True,change_char='@'):
    lines = text.split('\n')
    new = ''
    i = 0
    for line in lines:
        #第一行是不需要回车的
        if line == lines[0]:
            pass
        else:
            new += '\n'
        #if line == lines[-1] and not line:
            #break            
        if char in line:
            i = i+1
        else:
            new += line
            continue
        if auto_add:
            new += line.replace(char,new_char+str(i))
        else:
            new_char_now = new_char.replace(change_char,str(i))
            new = new + line.replace(char,new_char_now)
    return new

#TF翻转
#text    旧字符串
#must_same  全词匹配
def turn_TF(text='',must_same=False):
    if not must_same:
        text = text.replace('True','#@.true.@#')
        text = text.replace('False','#@.false.@#')
        text = text.replace('#@.true.@#','False')
        text = text.replace('#@.false.@#','True')
        return text
    else:
        text = '\n' + text + '\n'
        text = text.replace('\n',' \n ')
        text = text.replace(' True ','#@.true.@#')
        text = text.replace(' False ','#@.false.@#')
        text = text.replace('#@.true.@#',' False ')
        text = text.replace('#@.false.@#',' True ')
        text = text.replace(' \n ','\n')
        return text[1:-1]

#左右互换
#text    旧字符串
def trun_LR(text):
    lines = text.split('\n')
    return_text = ''        
    for line in lines:
        if line == lines[0]:
            pass
        else:
            return_text += '\n'
        try:
            key = re.findall('([\S\s]*=[\S\s]*)',line)[0]
        except Exception as e:
            return_text += line
        l_eq,r_eq = key.split('=')
        l,r = line.split(key)
        return_text = return_text + r + r_eq + '=' + l_eq + l + '\n'
    return return_text

#干掉开头空白
#text      旧字符串
def deleate_head(text=''):
    lines = text.split('\n')
    return_text = ''        
    for line in lines:
        if line == lines[0]:
            pass
        else:
            return_text += '\n'  
        try:
            key = re.findall('(^[ |]+)',line)[0]
        except:
            key = ''
        return_text = return_text + line.replace(key,'',1)
    return return_text

#干掉结尾空白
#text       旧字符串
def deleate_back(text):
    lines = text.split('\n')
    return_text = ''        
    for line in lines:
        if line == lines[0]:
            pass
        else:
            return_text += '\n'
        try:
            key = re.findall('(^[ |]+)',line[::-1])[0]
        except:
            key = ''
        return_text = return_text + line[::-1].replace(key,'',1)[::-1] 
    return return_text

#添加头
#text      旧字符串
#head      需要添加的头
def add_by_head(text='',head=''):
    _text = '\n' + text
    return _text.replace('\n','\n'+head)[1:]

#添加尾
#text      旧字符串
#head      需要添加的尾
def add_by_end(text='',end=''):
    if text[-1] == '\n':
        return text.replace('\n',end+'\n')
    else:
        _text = text + '\n'
        return _text.replace('\n',end+'\n')[:-1]

#符号对齐
#text 旧字符串
#symbols 字符关键字
def symbol_alignment(text='',symbols=''):
    #[\u4e00-\u9fa5]+ 正则也行
    _symbols = []
    __ = symbols.split(' ')
    for _ in __:
        if not _:
            continue
        else:
            _symbols.append(_)
    if text[-1] == '\n':
        text = text[:-1]
    #切割出来
    lline = []
    #登记每断的应当长度 
    maxlen = {}
    for key in _symbols:
        maxlen[key] = 0
    lines = text.split('\n')
    for line in lines:
        l = line
        split_list = []
        for key in _symbols:
            if key in l:
                s = l.split(key,1)
                split_list.append(s[0])
                l = s[1]
                the_len = (len(s[0].encode())-len(s[0]))//2 + len(s[0])   # encode中文长度会x3，但实际宽度是2
                if the_len > maxlen[key]:
                    maxlen[key] = the_len
            else:
                split_list.append('')
        split_list.append(l)
        lline.append(split_list)
    true_text = ''
    for line in lline:
        for key,s in zip(_symbols,line):
            r = '{:<%d}'%(maxlen[key]-(len(s.encode())-len(s))//2)
            true_text += r.format(s) + key
        true_text += line[-1] + '\n'
        
    
    
    
    
    return true_text
    for key in _symbols:
        lines = text.split('\n')
        if not lines[-1]:
            lines = lines[:-1]
        return_text = ''
        max_index = 0
        for line in lines:
            if line == lines[-1] and not line:
                break
            #for k in _symbols:
                #_r = '([ ]*{})'.format(k)
                #del_ks = re.findall(_r,line)
                #if del_ks:
                    #del_k = del_ks[0]
                    #line = line.replace(del_k,k)
            index = line.find(key)
            if index > max_index:
                max_index = index
        for line in lines:
            if line == lines[-1] and not line:
                break            
            if key in line:
                msg = line.split(key,1)
                return_text = return_text + msg[0] + ' '*(max_index-len(msg[0])) + key + msg[1] + '\n'
            else:
                return_text = return_text + line + '\n'
        text = return_text
    return text

#结尾空格对齐
#text 旧字符串
def end_alignment(text=''):
    lines = text.split('\n')
    return_text = ''
    max_len = 0
    for line in lines:
        if line == lines[-1] and not line:
            break
        if line[-1] == '\n':
            index = len(line) -1
        else:
            index = len(line)
        if index > max_len:
            max_len = index
    for line in lines:
        if line == lines[-1] and not line:
            break            
        return_text = return_text + line.replace('\n','') + ' '*(max_len-len(line.replace('\n',''))) + '\n'
    return return_text
