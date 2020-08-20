请输入年份：12
12 是闰年
year = int(input("请输入年份：")) 判断: 如果 year%4==0 and year%100!=0 or year%400==0 则  print(year,"是闰年"), 否则  
print(year,"不是闰年")
```flow
start=>start: start|past
inputoutput1=>inputoutput: year = int(input("请输入年份："))
condition2=>condition: if year%4==0 and year%100!=0 or year%400==0
inputoutput3=>inputoutput: print(year,"是闰年")
inputoutput4=>inputoutput: print(year,"不是闰年")
end=>end: end
start->inputoutput1
inputoutput1->condition2
condition2(yes)->inputoutput3
condition2(no)->inputoutput4
inputoutput3->end
inputoutput4->end
```

函数 equation () 的流程：  a = float(input("请输入系数a:")) b = float(input("请输入系数b:")) c = float(input("请输入系
数c:")) delta = b * b - 4 * a * c  判断: 如果 delta > 0 则  x1 = (-b + math.sqrt(delta)) / (2 * a) x2 = (-b - math.sqrt(delta)) / (2 * a) print("方程的两根为", x1, x2), 否则  print("方程没有实根")
```flow
start=>start: start
inputoutput5=>inputoutput: a = float(input("请输入系数a:"))
inputoutput6=>inputoutput: b = float(input("请输入系数b:"))
inputoutput7=>inputoutput: c = float(input("请输入系数c:"))
operation8=>operation: delta = b * b - 4 * a * c
condition9=>condition: if delta > 0
operation10=>operation: x1 = (-b + math.sqrt(delta)) / (2 * a)
operation11=>operation: x2 = (-b - math.sqrt(delta)) / (2 * a)
inputoutput12=>inputoutput: print("方程的两根为", x1, x2)
inputoutput13=>inputoutput: print("方程没有实根")
end=>end: end
start->inputoutput5
inputoutput5->inputoutput6
inputoutput6->inputoutput7
inputoutput7->operation8
operation8->condition9
condition9(yes)->operation10
operation10->operation11
operation11->inputoutput12
condition9(no)->inputoutput13
inputoutput12->end
inputoutput13->end
```

$\frac{4}{3}$