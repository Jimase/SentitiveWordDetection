import sys
from pypinyin import pinyin, Style
from hanzi_chaizi.hanzi_chaizi import HanziChaizi
from langconv import Converter
from Pinyin2Hanzi.Pinyin2Hanzi import DefaultHmmParams
from Pinyin2Hanzi.Pinyin2Hanzi import viterbi

#检验是否全是中文字符
def is_all_chinese(strs):
    for _char in strs:
        if not '\u4e00' <= _char <= '\u9fa5':
            return False
    return True

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

def get_fantizuhe(array1, array2, deepth, ans, noword):
    if deepth == len(array1):
        ans.append(noword)
        return
    for i in range(2):
        if i == 0:
            get_fantizuhe(array1, array2, deepth + 1, ans, noword + array1[deepth])
        elif i == 1:
            get_fantizuhe(array1, array2, deepth + 1, ans, noword + array2[deepth])

def get_fpyzu(array1, array2, deepth, ans, noword):
    if deepth == len(array1):
        ans.append(noword)
        return
    for i in range(2):
        if i == 0:
            get_fpyzu(array1, array2, deepth + 1, ans, noword + array1[deepth])
        elif i == 1:
            get_fpyzu(array1, array2, deepth + 1, ans, noword + array2[deepth])

def get_xieyinzuhe(array, deepth, ans, noword):
    if deepth == len(array):
        ans.append(noword)
        return
    for i in range(len(array[deepth])):
        get_xieyinzuhe(array, deepth + 1, ans, noword + array[deepth][i])

# DFA算法
class DFAFilter(object):
    # 构造函数的参数为关键词文件路径
    def __init__(self, senstive_path, result_path):
        # 关键词字典
        self.keyword_chains = {}
        # 限定读
        self.delimit = '\x00'
        self.parse(senstive_path)
        self.result_path = result_path
        self.total = 0
        self.rp = open(self.result_path, "w", encoding="utf-8")
        self.filestr = ""

    # 向关键词字典中插入关键字
    def add(self, keyword, rawkeyword):
        # 关键词英文变为小写
        chars = keyword.lower()
        if not chars: return
        level = self.keyword_chains
        # 遍历关键字的每个字
        for i in range(len(chars)):
            # 如果这个字已经存在字符链的key中就进入其子字典
            if chars[i] in level:
                level = level[chars[i]]
            else:
                if not isinstance(level, dict):
                    break

                for j in range(i, len(chars)):
                    level[chars[j]] = {}
                    last_level, last_char = level, chars[j]
                    level = level[chars[j]]
                last_level[last_char] = {self.delimit: rawkeyword}
                # break
                return
        if i == len(chars) - 1:
            level[self.delimit] = chars
        # level = {self.delimit: rawkeyword}

    # 构建关键词字典
    def parse(self, path):
        with open(path, encoding='utf-8') as f:
            for keyword in f.readlines():
                ckeyword = keyword.strip()
                if is_all_chinese(ckeyword):
                    # 构建拼音敏感字
                    x = pinyin(ckeyword, style=Style.NORMAL)
                    pkeyword = [item[0] for item in x]
                    # print("pkeyword", pkeyword)
                    ans = []
                    get_permutation(ckeyword, pkeyword, 0, ans, [])
                    for ansitem in ans:
                        tkeyword = ""
                        for item in ansitem:
                            tkeyword += item
                        self.add(tkeyword, ckeyword)

                    # 得到首字母类型的拼音
                    py = pinyin(ckeyword, style=Style.FIRST_LETTER)
                    fpy = ""
                    for item in py:
                        fpy += item[0]
                    fpzu = []
                    get_fpyzu(ckeyword, fpy, 0, fpzu, "")
                    for item in fpzu:
                        # print(item)
                        self.add(item, ckeyword)

                    # 首字母拼音和全拼音组合
                    ans = []
                    get_fpyzu(fpy, pkeyword, 0, ans, "")
                    for item in ans:
                        self.add(item, ckeyword)

                    # 构建谐音敏感字
                    # 首先得到文字的拼音
                    py =  pinyin(ckeyword, style=Style.NORMAL)
                    hmmparams = DefaultHmmParams()
                    xieyin = []
                    for item in py:
                        result = viterbi(hmm_params=hmmparams, observations=(item), path_num=15)
                        xieyin.append([item2.path[0] for item2 in result])
                    xieyinzuhe = []
                    get_xieyinzuhe(xieyin, 0, xieyinzuhe, "")
                    for item in xieyinzuhe:
                        # print(item)
                        self.add(item, ckeyword)

                    # # 得到谐音加拼音敏感字
                    # for item in xieyinzuhe:
                    #     ans = []
                    #     get_fpyzu(item, fpy, 0, ans, "")
                    #     # print(ans)
                    #     for item2 in ans:
                    #         if item2 == "法伦g":
                    #             print("YYYYYYY")
                    #             print(ans)
                    #         self.add(item2, ckeyword)

                    # 构建部首敏感字
                    hc = HanziChaizi()
                    bushou = []
                    for item in ckeyword:
                        ans = hc.query(item)
                        bushou.append(ans)
                    ans = []
                    get_bushouword(bushou, 0, ans, "")
                    for bushouword in ans:
                        self.add(bushouword, ckeyword)

                    # 构建繁体字字典
                    fanti = chs_to_cht(ckeyword)
                    fjti = []
                    get_fantizuhe(fanti, ckeyword, 0, fjti, "")
                    for item in fjti:
                        self.add(item, ckeyword)
                else:
                    self.add(ckeyword, ckeyword)
            # print(self.keyword_chains)

    # 根据关键字字典过滤出输入字符串message中的敏感词
    def filter(self, message, linenumber):
        rawmessage = message
        message = message.lower()
        start = 0
        while start < len(message):
            level = self.keyword_chains
            # 当字符不在关键字字典时
            if message[start] not in level:
                start += 1
                continue
            if is_all_chinese(message[start]): mode = "c"
            else: mode = "e"
            step_ins = 0
            sensitive_word = ""
            left, right = start, 0
            ok = False
            for char in message[start:]:
                if char.isdigit():
                    step_ins += 1
                    continue
                if char not in level and mode == "c" and char.encode("utf-8").isalpha():
                    step_ins += 1
                    continue
                # 特殊字符判断，当一个字符既不是中文又不是英文和数字时被认定为为特殊字符
                if not is_all_chinese(char) and not char.encode("utf-8").isalpha()\
                    and not char.isdigit():
                    step_ins += 1
                    continue
                # 新字在敏感词字典链表中
                if char in level:
                    # sensitive_word += char
                    step_ins += 1
                    # 特定字符不在当前字的value值里，嵌套遍历下一个
                    if self.delimit not in level[char]:
                        level = level[char]
                    else:
                        start += step_ins - 1
                        right = start
                        ok = True
                        sensitive_word = level[char][self.delimit]
                        break
                # 新字不在敏感词字典链表中
                else: break
            if ok:
                anstr = "Line{}: <{}> {}\n".format(linenumber, sensitive_word, rawmessage[left: right + 1])
                self.filestr += anstr
                print(anstr, end="")
                # self.rp.write(anstr)
                self.total += 1
            start += 1

    def __del__(self):
        self.rp.write("Total: " + str(self.total) + '\n')
        self.rp.write(self.filestr)
        self.rp.close()

def main(word_path, file_path, result_path):
    # 关键词文件路径
    # word_path = "./data/words.txt"
    dfa = DFAFilter(word_path, result_path)
    # 待解析文本路径
    # article_path = "./data/org.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for index in range(len(lines)):
            dfa.filter(lines[index], index + 1)
    print(dfa.total)

if __name__ == '__main__':
    print(sys.argv)
    print(len(sys.argv))
    if len(sys.argv) != 4:
        print("参数错误，请以此给出敏感词文件，待检测文件和结果文件")
        exit(-1)
    args = sys.argv
    main(args[1], args[2], args[3])
