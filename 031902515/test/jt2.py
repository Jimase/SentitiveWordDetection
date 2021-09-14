from pypinyin import pinyin, Style
import copy
from hanzi_chaizi.hanzi_chaizi import HanziChaizi

def fun1():
    x = pinyin("法轮功", style=Style.NORMAL)
    print(x)
    print(type(x))
    print(type(x[0]))
    print(x[0])
    print(x[0][0])
    print(type(x[0][0]))

def get_permutation(cstr, pstr, deepth, ans, nowlist):
    if deepth == len(cstr):
        # print(nowlist)
        ans.append(nowlist)
        # print("ans: ", ans)
        return
    for i in range(2):
        if i == 0:
            # nowlist.append(cstr[deepth])
            get_permutation(cstr, pstr, deepth + 1, ans, nowlist + [cstr[deepth]])
            # del nowlist[len(nowlist) - 1]
        elif i == 1:
            # nowlist.append(pstr[deepth])
            get_permutation(cstr, pstr, deepth + 1, ans, nowlist + [pstr[deepth]])
            # del nowlist[len(nowlist) - 1]
    return

def get_bushouword(bushoulist, deepth, ans, noword):
    if deepth == len(bushoulist):
        ans.append(noword)
        return
    for bushou in bushoulist[deepth]:
        sigleword = ""
        for item in bushou:
            sigleword += item
        get_bushouword(bushoulist, deepth + 1, ans, noword + sigleword)

def fun2():
    cstr = "法轮功"
    x = pinyin(cstr, style=Style.NORMAL)
    pstr = [item[0] for item in x]
    print(cstr)
    print(pstr)
    ans = []
    get_permutation(cstr, pstr, 0, ans, [])
    print(ans)
    for ansitem in ans:
        print("ansitem: ", ansitem)
        keyword = ""
        for item in ansitem:
            keyword += item
        print(keyword)

def fun3():
    # x = "nihao"
    hc = HanziChaizi()
    ans = hc.query("教")
    print(ans)

def fun4():
    hc = HanziChaizi()
    keyword = "邪教"
    bushou = []
    for item in keyword:
        ans = hc.query(item)
        bushou.append(ans)
    print(bushou)
    ans = []
    get_bushouword(bushou, 0 , ans, "")
    print(ans)

if __name__ == '__main__':
    # fun1()
    # fun2()
    # fun3()
    fun4()