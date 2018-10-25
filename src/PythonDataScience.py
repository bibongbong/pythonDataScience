#   map()
#   根据提供的函数对指定序列做映射
#   map(function, iterable, ...)
people = ['Dr. Christopher Brooks',
          'Dr. Kevyn Collins-Thompson',
          'Dr. VG Vinod Vydiswaran',
          'Dr. Daniel Romero']
import re
def split_title_and_name(person):
    words = re.split(r'(\.|\s)', person)
    return words[0]+words[1]+words[-1]
print(list(map(split_title_and_name, people)))
print(list(map(lambda x:x.split()[0]+" "+ x.split()[-1], people)))


#   列表推导
my_list = [i for i in range(0, 100) if i%2 == 0]
print(my_list)

#   双重循环的列表推导
def times_tables():
    lst = []
    for i in range(10):
        for j in range (10):
            lst.append(i*j)
    return lst

times_tables() == [i*j for i in range(0,10) for j in range(0,10)]


# Many organizations have user ids which are constrained in some way.
# Imagine you work at an internet service provider and the user ids
# are all two letters followed by two numbers (e.g. aa49).
# Your task at such an organization might be to hold a record
# on the billing activity for each possible user.

# Write an initialization line as a single list comprehension
# which creates a list of all possible user ids.
# Assume the letters are all lower case.
lowercase = 'abcdefghijklmnopqrstuvwxyz'
digits = '0123456789'

# answera还是带有浓重的c的风格
answera = [lowercase[i]+lowercase[j]+digits[m]+digits[n]
           for i in range(26) for j in range(26)
           for m in range(10) for n in range(10)]
answerb = [a+b+c+d for a in lowercase for b in lowercase for c in digits for d in digits]
#print(answera == answerb)


import numpy as np

# creating arrays
mylist = [1,2,3]
x = np.array(mylist)
print(x)

y = np.array([4,5,6])
z = np.array([[7,8,9],[10,11,12]])

print(z.shape)  # (2,3)  表示z是2x3的矩阵

n = np.arange(0,30,2) # 用arange生成一个矩阵，值从0~30，step为2
m = n.reshape(3,5)  # 把矩阵n转换为3x5
print(m)

a = np.linspace(0, 4, 9)  # linspace和arange相似，把0~4均匀间隔的9个数
b = a.reshape(3,3)
print(b)

zeroarray = np.zeros((3,3))#定义一个3x3的0矩阵,必须以元组（3,3） 作为入参，而不是两个参数3,3

print(zeroarray)
ones = np.ones((3,3))#定义一个3x3的1矩阵
print(ones)

print(np.vstack([ones, 3*ones]))    # np.vstack()一个入参，是数组[a,b], 作用是把矩阵a(3x3)和b(3x3)在行方向叠加，生成(6x3)
print(np.hstack([ones, 3*ones]))    # np.vstack()一个入参，是数组[a,b], 作用是把矩阵a(3x3)和b(3x3)在列方向叠加，生成(3x6)


print(x**2)     # [1 4 9]
print(x+y)      # [5 7 9]
print(x*y)      # [4 10 18]
print(x.dot(y)) # 32, x和y中每个元素相乘然后积再相加， 1*4+2*5+3*6=32

z = np.array([y,y**2])
print(z)
print(z.T)  # z.T 表示将z转置，z是2x3, z.T是3x2

a = np.array([-4,-2,1,3,5])
print("a = [-4,-2,1,3,5] ")
print("a.sum() ",a.sum())   #   3
print("a.max() ",a.max())   #   5
print("a.min() ",a.min())   #   -4
print("a.argmax() ",a.argmax()) #   4  argmax()返回最大元素的index
print("a.argmin() ",a.argmin()) #   0  argmin()返回最小元素的index



#  Indexing/Slicing
s = np.arange(13)**2    #   [  0   1   4   9  16  25  36  49  64  81 100 121 144]
print("s[0]={}, s[4]={}, s[0:3]={}".format(s[0], s[4], s[0:3])) #   s[0]=0, s[4]=16, s[0:3]=[0 1 4]
print("s[-5::-2]= {}".format(s[-5::-2]))    #   s[-5::-2]= [64 36 16  4  0]

r = np.arange(36)
r.resize(6,6)
#[[ 0  1  2  3  4  5]
# [ 6  7  8  9 10 11]
# [12 13 14 15 16 17]
# [18 19 20 21 22 23]
# [24 25 26 27 28 29]
# [30 31 32 33 34 35]]
print(r[2,2])   #   14  取第三行第三列的元素
print(r[3, 3:6]) #  [21,22,23]  取第三行的第4个到第7个元素
print(r[:2, :-1])  #    取从第一行到第二行的第一个到最后一个元素
print(r[r>30] )     #   取所有大于30的元素
r[r>30] = 30    # 给所有大于30的元素重新赋值为30
r2 = r[:3,:3]   # 取r的前三行前三列，
r2[:] = 0       # r2 所有元素赋值为0，r2为这个子矩阵的索引，对r2的改变，也就是对r的改变
r_copy = r.copy() # 这个r_copy为r矩阵的拷贝，是另一个全新对象，对r_copy的修改，不会影响到r


# 高级索引之整数数组索引
#   高级索引始终返回数据的副本
#   获取数组中(0,0)，(1,1)和(2,0)位置处的元素。
x = np.array([[1,2], [3,4], [5,6]])
y = x[[0,1,2],[0,1,0]]  #   行列索引是1维，得到的结果也是一维
print("整数数组索引")
print(y)

#   获取了 4X3 数组中的四个角的元素。
# [ 0  1  2]
# [ 3  4  5]
# [ 6  7  8]
# [ 9 10 11]
# 行索引是
# [ 0, 0]
# [ 3, 3]
# 而列索引是
# [ 0, 2]
# [ 0 ,2]
# 行列索引是二维，得到的结果也是二维，有点像行列索引矩阵合并成如下：
# [ 0:0, 0:2]
# [ 3:0, 3:2]
# 取四个元素的位置为 0,0  0,2  3,0  3,2
x = np.array([[ 0, 1, 2],[ 3, 4, 5],[ 6, 7, 8],[ 9, 10, 11]])
print("x:\n",x)
rows = np.array([[0,0],[3,3]])
cols = np.array([[0,2],[0,2]])
y = x[rows,cols]
# y的结果
# [[ 0  2]
# [ 9 11]]
print("y:\n",y)
#   所以如果我们要取 3/4/6/7时
#   就可以先列出行索引,也就是四个元素的行号，你想得到的结果是2x2，那么行索引也是2x2, [[1,1],[2,2]]
#   四个元素的列索引，[0,1] [0,1]
#z:
# [[3 4]
# [6 7]]
rows = np.array([[1,1],[2,2]])
cols = np.array([[0,1],[0,1]])
z = x[rows,cols]
print("z:\n",z)