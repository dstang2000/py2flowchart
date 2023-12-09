import math
import os
import pytest

from core import * 

# if you want to show a flowchart, please visit:
# https://flowchart.js.org

#@with_flowchart
def myfun():
    c = 9
    while c<10:
        c-=1
        if c>0:
            print(c)
            print(c)
        else:
            print(c+1)
        c-=2
    return c

#@with_flowchart
def myfun2(a, b):
    print(a, b)
    c = a * b

    for i in range(a, b):
        print(i)
        for j in [1, 2, 3]:
            if j>3:
                break
            print(j)
        print(i, "in for")
    while i < b + 5:
        print(i * i)
        print(i + 2)
    if a > b:
        print(a)
        c = a * a
    elif a > 0:
        d = b * b
    elif b > 0:
        d2 = b**3
        for k, j in {}.items():
            print(k, j)
    else:
        d3 = 100
        d4 = 1000
    return a + b

def equation():
    a = float(input("请输入系数a:"))
    b = float(input("请输入系数b:"))
    c = float(input("请输入系数c:"))

    delta = b * b - 4 * a * c
    if delta > 0:
        x1 = (-b + math.sqrt(delta)) / (2 * a)
        x2 = (-b - math.sqrt(delta)) / (2 * a)
        print("方程的两根为", x1, x2)
    else:
        print("方程没有实根")


def test_module():
    # 测试模块导入
    modulename = r"if_leap_year"
    mdl = __import__(modulename)
    s = get_flowchart(mdl)
    print(s)

    # 测试直接用代码文本
    with open(modulename + ".py", "r", encoding="utf-8") as f:
        src = f.read()
    assert get_flowchart(src)

    print("writefile")
	
    pyfile2flowchart("if_leap_year.py", "if_leap_year.html", {"line-width":2})
    assert os.path.exists("if_leap_year.html")

print("======== test module 222 ======")

test_module()
print("======== test module end ======")

#print(myfun)

# 测试函数
def test_fun():
    s = get_flowchart(myfun)
    assert s
    assert get_flowchart(myfun2)
    assert get_flowchart(equation)

test_fun()

mycode="""
s = 1
f = 1
sgn = 1
for n in range(1,101):
    sgn *= -1
    f = sgn /(2*n+1)
    s += f
print(s*4)
"""
print(get_flowchart(mycode))


def mypi():
	s = 1
	f = 1
	sgn = 1
	for n in range(1,101):
		sgn *= -1
		f = sgn /(2*n+1)
		s += f
	print(s*4)
print(get_flowchart(mypi))


def print_sorted(dct):
    result = sorted(dct.items())
    for k, v in result:
        print(k, v)

def statistics():
    txt = "hello"
    dct = {}
    for c in txt:
        if c in dct:
            dct[c] += 1
        else:
            dct[c] = 1
    print(dct)
    print_sorted(dct)
    
print(get_flowchart(statistics))
print(get_flowchart(print_sorted))

