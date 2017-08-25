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

#@property:请利用@property给一个Screen对象加上width和height属性，以及一个只读属性resolution
class Screen(object):
    @property
    def width(self):
        return self._width

    @property
    def height(self):
        return self._height

    @width.setter
    def width(self, value):
        # 宽度值判断
        if not isinstance(value, (int,float)):
            raise ValueError('width must be an integer or float!')
        if value < 0:
            raise ValueError('width must > 0')
        self._width = value

    @height.setter
    def height(self, value):
        # 高度值判断
        if not isinstance(value, (int, float)):
            raise ValueError('height must be an integer or float!')
        if value < 0:
            raise ValueError('height must > 0')
        self._height = value

    @property
    def resolution(self):
        return self._width * self._height

s = Screen()
s.width = 1024
s.height = 768
print(s.resolution)
assert s.resolution == 786432, '1024 * 768 = %d ?' % s.resolution
</pre>