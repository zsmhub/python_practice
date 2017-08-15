# python_practice
廖雪峰老师的练习题

<pre>
#列表生成式
L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = [s.lower() for s in L1 if isinstance(s, str)]   # 先for循环，再if筛选，再s.lower
print("L2:", L2) # 输出: ['hello', 'world', 'apple']
L3 = [s.lower() if isinstance(s, str) else s for s in L1]   # 先for循环，再if筛选（True则s.lower，False则返回s）
print("L3:", L3) # 输出: ['hello', 'world', 18, 'apple', None]

#生成器-杨辉三角
def triangles():
    L=[1]
    while True:
        yield L
        L = [1] + [ L[x-1] + L[x] for x in range(1,len(L)) ] + [1] # +号用于组合列表

i = 0
for x in triangles():
    print(x)
    i += 1
    if i == 10:
        break
</pre>