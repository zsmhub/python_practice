# python_practice
廖雪峰老师的练习题

<pre>
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