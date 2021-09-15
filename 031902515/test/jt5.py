#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@Author: Victor
@Contact: 、@163.com
@Date: 2020/9/18
@function: ''
'''

from langconv import Converter
from pypinyin import pinyin, Style
from Pinyin2Hanzi.Pinyin2Hanzi import DefaultHmmParams
from Pinyin2Hanzi.Pinyin2Hanzi import viterbi

def cat_to_chs(sentence):  # 传入参数为列表
    """
    将繁体转换成简体
    :param line:
    :return:
    """
    sentence = ",".join(sentence)
    sentence = Converter('zh-hans').convert(sentence)
    sentence.encode('utf-8')
    return sentence.split(",")

def chs_to_cht(sentence):  # 传入参数为列表
    """
    将简体转换成繁体
    :param sentence:
    :return:
    """
    sentence = ",".join(sentence)
    sentence = Converter('zh-hant').convert(sentence)
    sentence.encode('utf-8')
    return sentence.split(",")

def fun1():
    li_1 = ['鸡', '鸡', '虎', '牛', '猪', '虎', '兔']
    li_2 = ['雞', '雞', '虎', '牛', '豬', '虎', '兔']
    rest_fon = chs_to_cht(li_1)  # 简体转换成繁体
    print("简体转换成繁体:{0}".format(rest_fon))

    rest_chinese = cat_to_chs(li_2)
    print("简体转换成简体:{0}".format(rest_chinese))

def fun2():
    chstr = "法轮功"
    print(chs_to_cht(chstr))

def fun3():
    cstr = "法轮功"
    ans = pinyin(cstr, style=Style.FIRST_LETTER)
    fans = ""
    for item in ans:
        fans += item[0]
    print(ans)
    print(fans)

def fun4():
    cstr = "法轮功"
    x = pinyin(cstr, style=Style.NORMAL)
    print(x)
    hmmparams = DefaultHmmParams()
    xieyin = []
    ## 2个候选
    for item in x:
        result = viterbi(hmm_params=hmmparams, observations=(item), path_num=15)
        xieyin.append([item2.path[0] for item2 in result])
        for item2 in result:
            print(item2.path)
    print(xieyin)
    # print(xieyin.shape)

if __name__ == '__main__':
    # fun1()
    # fun2()
    # fun3()
    fun4()