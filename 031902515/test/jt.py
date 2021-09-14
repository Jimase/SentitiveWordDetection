# from mian import is_all_chinese

def fun1():
    while 1:
        x = str(input()).strip()
        if x == "exit": break
        print(is_all_chinese(x))

def fun2():
    s = "123"
    print(s.encode("utf-8").isalpha())

def fun3(a):
    if not (a < 3):
        print("yes")

def fun4():
    s = "你好"
    print(s.isdigit())

if __name__ == '__main__':
    # fun1()
    # fun2()
    # fun3(5)
    fun4()