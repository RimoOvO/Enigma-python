# Enigma-python
一个通过Python（3.0+）实现的3转子恩格玛机，通过命令行或文件进行交互

## Usage
1. 生成一个新的转子序列: `python Enigma.py --init`

   他将会生成一个配置文件`rotor.ini`来保存转子序列、转子编码和反射器序列
   
   参数优先级：命令行参数>配置文件参数>内部默认值
   
2. 从命令行加解密信息: `python Enigma.py -t <文本> [-c <转子编码> -r1 <转子1序列> -r2 <转子2序列> -r3 <转子3序列> -re <反射器序列>]`

   中括号内的内容都是可选的，如果为空，那么将从配置文件中读取
   
   文本值只可以是`26个小写字母`和`空格`，转子编码为6位，从`000000`到`999999`
   
   转子1-3的序列为打乱的26个小写字母；反射器序列中，区域的字母两两相互映射，如a->k,k->a，顺序序列为a-z
   
3. 从文件中加解密: `python Enigma.py -i <输入文件名> [-o <输出文件名> ...(省略的参数同第二条中括号内的参数)]`
   
   从文件中加解密将会删去原文中所有的空格后输出

## ToDo
1. 恢复解码空格

2. 多转子兼容

3. 实现接线板
