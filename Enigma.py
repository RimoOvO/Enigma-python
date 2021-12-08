# -*- coding: utf-8 -*-
import argparse
import configparser
import re
import os.path
import random

def simple_replace(password, replace_word1, replace_word2, replace_word3, replace_word):  # 加密的主函数
    count = 0  # 设置计数器
    new_pass = ''  # 设置一个空字符串准备接收密码
    ori_table = 'abcdefghijklmnopqrstuvwxyz'  # 原始的字符串，用来建立映射表
    reverse_table = str.maketrans(ori_table, replace_word)
    for obj in password:  # 开始拆解原字符串
        table1 = str.maketrans(ori_table, replace_word1)  # 建立转子1的映射表
        table2 = str.maketrans(ori_table, replace_word2)  # 建立转子2的映射表
        table3 = str.maketrans(ori_table, replace_word3)  # 建立转子3的映射表
        new_obj = str.translate(obj, table1)  # 把obj通过转子1转换
        new_obj = str.translate(new_obj, table2)  # obj通过转子2
        new_obj = str.translate(new_obj, table3)  # obj通过转子3
        new_obj = reverse_word(new_obj, reverse_table)  # 进入自反器，得到自反值
        reverse_table1 = str.maketrans(
            replace_word1, ori_table)  # 增加自反出去的对应表，反向解译
        reverse_table2 = str.maketrans(replace_word2, ori_table)
        reverse_table3 = str.maketrans(replace_word3, ori_table)
        # new_obj再赋值，反向解译通过转子3
        new_obj = str.translate(new_obj, reverse_table3)
        new_obj = str.translate(new_obj, reverse_table2)  # 通过转子2
        new_obj = str.translate(new_obj, reverse_table1)  # 通过转子1
        new_pass += new_obj  # 返回的密码增加一个new_obj

        replace_word1 = rotors(replace_word1)  # 转子1每个字符都转动一次
        count += 1  # 计数器增加1
        if count % 676 == 0:   # 如果模676为0，那么转子3转动一次(因为转子2已经转动了一整圈）
            replace_word3 = rotors(replace_word3)
        elif count % 26 == 0:  # 如果模26为0，那么转子2转动一次（因为转子1已经转动了一整圈）
            replace_word2 = rotors(replace_word2)
    return new_pass  # 返回新的已经被转子加密的密码

def is_str(password, replace_word1, replace_word2, replace_word3):  # 判断的函数
    an = re.match('[a-z]+$', password)  # 当时的enigma机是没有空格的，所以这里要求输入的明文也必须是小写字母
    if not type(password) == type(replace_word1) == type(replace_word2) == type(replace_word3) == type('a'):
        print('密码必须是字符串！')
        return False
    elif not an:
        print('字符串只能包含小写字母！')
        return False
    elif not len(replace_word1) == len(replace_word2) == len(replace_word3) == 26:
        print('替换码必须为26个字母！')
        return False
    else:
        return True  


def rotors(replace_word):  # 转子转动的函数，每调用一次，就把转子前面第一个字母移动到最后
    return replace_word[1:] + replace_word[0]


def reverse_word(word, reverse_table):  # 自反器
    return str.translate(word, reverse_table) # 把输入的字母根据映射表调换


def preSetup():
    # 初始化
    global conf
    conf = configparser.ConfigParser()

    global parser
    parser = argparse.ArgumentParser(description="Enigma.")
    parser.add_argument('-t', '--text', default='',help=argparse.SUPPRESS) # 参数文本
    parser.add_argument('-c', '--code', default='',help=argparse.SUPPRESS) # 参数转子编码
    parser.add_argument('-r1', '--rotor1', default='',help=argparse.SUPPRESS) # 转子1序列
    parser.add_argument('-r2', '--rotor2', default='',help=argparse.SUPPRESS) # 转子2序列
    parser.add_argument('-r3', '--rotor3', default='',help=argparse.SUPPRESS) # 转子3序列
    parser.add_argument('-re', '--reflector', default='',help=argparse.SUPPRESS) # 反射器序列
    parser.add_argument('-i', '--input', default='',help=argparse.SUPPRESS) # 输入文件名
    parser.add_argument('-o', '--output', default='',help=argparse.SUPPRESS) # 输出文件名
    parser.add_argument('--init', action='store_true', default=False) # 激活init()函数
    global args
    args = parser.parse_args()

    return 0


def loadRotor():

    conf_rotor1, conf_rotor2, conf_rotor3, conf_code, conf_replace_word = loadConf()

    if args.rotor1 != '': # 决定转子1的序列来自哪里
        r_password1 = args.rotor1
        print('转子1序列来自参数： ',r_password1)
    elif conf_rotor1 != '':
        r_password1 = conf_rotor1
        print('转子1序列来自配置文件： ',r_password1)
    else:
        r_password1 = 'njafkzurywldtsgocxbeqpivmh'  
        print('转子1序列使用默认值： ',r_password1)

    if args.rotor2 != '': # 决定转子2的序列来自哪里
        r_password2 = args.rotor2
        print('转子2序列来自参数： ',r_password2)
    elif conf_rotor2 != '':
        r_password2 = conf_rotor2
        print('转子2序列来自配置文件： ',r_password2)
    else:
        r_password2 = 'tbfhpeqngmsjoukydlvxzirawc'  
        print('转子2序列使用默认值： ',r_password2)

    if args.rotor3 != '': # 决定转子3的序列来自哪里
        r_password3 = args.rotor3
        print('转子3序列来自参数： ',r_password3)
    elif conf_rotor3 != '':
        r_password3 = conf_rotor3
        print('转子3序列来自配置文件： ',r_password3)
    else:
        r_password3 = 'jznymxapvbtkurflwgsohqedci'  
        print('转子3序列使用默认值： ',r_password3)

    if args.reflector != '': # 决定反向器的序列来自哪里
        replace_word = args.reflector
        print('反向器序列来自参数： ',replace_word)
    elif conf_replace_word != '':
        replace_word = conf_replace_word
        print('反向器序列来自配置文件： ',replace_word)
    else:
        replace_word = 'ykgwjmcrpebsftziuhlnqxdvao'  
        print('反向器序列使用默认值：',replace_word)

    if args.code != '': # 决定转子编码来自哪里
        code = args.code
        if len(code) != 6:
            print('无效的转子编码')
            exit()
        print('转子编码来自参数： ',code)
    elif conf_code!= '':
        code = conf_code
        print('转子编码来自配置文件： ',code)
    else:
        code = '000000'  # code
        print('转子编码使用默认值： ',code)

    return r_password1, r_password2, r_password3, code, replace_word


def preRoll(r_password1,r_password2,r_password3,code : str):
    # 把转子转到设定的位置
    roll3 = int(code[:2])
    roll2 = int(code[2:4])
    roll1 = int(code[4:])

    for i in range(roll1): # 转几次就循环几次
        r_password1 = rotors(r_password1)
    for i in range(roll2):
        r_password2 = rotors(r_password2)
    for i in range(roll3):
        r_password3 = rotors(r_password3)

    return r_password1, r_password2, r_password3


def loadConf():
    if not os.path.exists('rotor.ini'):
        return '','','','',''

    conf.read('rotor.ini')
    conf_rotor1 = conf.get('rotor', 'rotor1')
    conf_rotor2 = conf.get('rotor', 'rotor2')
    conf_rotor3 = conf.get('rotor', 'rotor3')
    conf_code = conf.get('rotor', 'code')
    conf_replace_word = conf.get('rotor', 'reverse')
    return conf_rotor1, conf_rotor2, conf_rotor3, conf_code, conf_replace_word

def readFile():
    # 从文件读取文本
    file_name = args.input
    if not os.path.exists(file_name):
        print('无效的文件名')
        exit()
    with open(file_name, 'r', encoding='utf-8') as f:
        text = f.read()
    text = text.replace(' ','') # 删除文本中所有空格
    return text

def getText():
    # 决定到底从哪里获取待编码的文本
    if args.text != '':
        text = args.text # 从参数
    elif args.input != '':
        return readFile() # 从文件
    else: 
        text = '0' # 没有文本，返回‘0’
    return text

def shuffleStr(s):
    # 随机打乱一个字符串
    str_list = list(s)
    random.shuffle(str_list)
    return ''.join(str_list)

def newReverse():
    # 生成一个新的反射器序列
    # 要求：两两相互映射，如a->k,k->a，顺序序列为a-z
    reverse_list = list('aaaaaaaaaaaaaaaaaaaaaaaaaa') # 转换成列表
    origin_list = list('abcdefghijklmnopqrstuvwxyz')

    for i in range(13): # 只需要循环一半的次数，也就是13次
        pick1 = origin_list[random.randint(0,len(origin_list)-1)] # 26个字母中随机取一个
        origin_list.remove(pick1) # 删掉他
        pick2 = origin_list[random.randint(0,len(origin_list)-1)] # 剩下25个字母再随机取一个
        origin_list.remove(pick2) # 再删掉他
        reverse_list[ord(pick1)-97] = pick2 # 放在新列表的两者对应位置
        reverse_list[ord(pick2)-97] = pick1 # 和上方对应

    return ''.join(reverse_list) # 转换回字符串

def init():
    # 生成新的转子、反射器序列和转子编码
    if args.init == True:
        code = str(random.randint(0,999999)).zfill(6)
        rotor1 = shuffleStr('abcdefghijklmnopqrstuvwxyz') # 打乱26个字母
        rotor2 = shuffleStr('abcdefghijklmnopqrstuvwxyz')
        rotor3 = shuffleStr('abcdefghijklmnopqrstuvwxyz')
        reverse = newReverse()

        conf.read('rotor.ini') # 写入配置文件
        conf.set('rotor', 'code', code)
        conf.set('rotor', 'rotor1', rotor1)
        conf.set('rotor', 'rotor2', rotor2)
        conf.set('rotor', 'rotor3', rotor3)
        conf.set('rotor', 'reverse', reverse)
        conf.write(open('rotor.ini', 'w'))

        print('生成了新的转子编码、转子序列和反射器序列')
        exit()
    return 0


if __name__ == '__main__':
    preSetup() # 初始化
    init() # 生成新的序列
    a_password = getText() 
    r_password1, r_password2, r_password3, code, replace_word = loadRotor()
    r_password1, r_password2, r_password3 = preRoll(r_password1,r_password2,r_password3,code)

    if is_str(a_password, r_password1, r_password2, r_password3):
        new_pass = simple_replace(a_password,r_password1, r_password2, r_password3, replace_word)
        print('密文/明文如下：', new_pass)
    if args.output != '' :
        with open(args.output, 'w+') as f:
            f.write(new_pass)
        print('保存了输出到文件：',args.output)