import pandas as pd

# DataFrame的结构

purchase1 = pd.Series({'Name':'Chris',
                       'Item purchased':'Dog Food',
                       'Cost':22.50})


purchase2 = pd.Series({'Name':'Kevyn',
                       'Item purchased':'Kitty Litter',
                       'Cost':2.50})

purchase3 = pd.Series({'Name':'Vinod',
                       'Item purchased':'Bird Seed',
                       'Cost':5.00})

# 注意，这里index里的第一项和第二项都是‘store1’,表示都是来自同一个商店
df = pd.DataFrame([purchase1,purchase2,purchase3], index=['store1','store1','store2',])
print(df.head())

#         Cost Item purchased   Name
# store1  22.5       Dog Food  Chris
# store1   2.5   Kitty Litter  Kevyn
# store2   5.0      Bird Seed  Vinod


# DataFrame和Series一样，也可以通过loc和iloc去取值，但对DataFrame来说返回的是一个列表
# loc和iloc是属性，不是方法，应该用[ ]，不能用()
print(df.loc['store2'])
# Cost                         5
# Item purchased       Bird Seed
# Name                     Vinod
# Name: store2, dtype: object
print(type(df.loc['store2']))   # <class 'pandas.core.series.Series'>
print(type(df))   # <class 'pandas.core.frame.DataFrame'>

# 要记住，索引（index）和列（cloumn)，沿着垂直或者水平的轴可能不是唯一的，
# 在这个例子里，index ‘store1' 有两行，所以loc['store1']返回的是一个新的DataFrame
print(df.loc['store1'])
#         Cost Item purchased   Name
# store1  22.5       Dog Food  Chris
# store1   2.5   Kitty Litter  Kevyn

## 如果要得到所有被买到的东西， 两种方法结果一样，但方法二更好, 方法三是把DataFrame转置
## index感觉就是另外再加上去的，purchase1/purchase2/purchase3 本身就可以直接操作，但只能按cloumn去取
#  Cost Item purchased   Name
#  22.5       Dog Food  Chris
#  2.5    Kitty Litter  Kevyn
#  5.0       Bird Seed  Vinod
print(df.loc[:]['Item purchased']) # 方法1
print(df['Item purchased'])    # 方法2
print(df.T.loc['Item purchased'])  # 方法3，可以用但是很丑
#                   store1        store1     store2
# Cost                22.5           2.5          5
# Item purchased  Dog Food  Kitty Litter  Bird Seed
# Name               Chris         Kevyn      Vinod

#print(df['Item purchased'][0]) # 错误

# DataFrame的优势就是可以方便在多个轴向去操作数据
# 想取store1的所有花费,两种方式都可以
print(df.loc['store1','Cost'])
#print(df.loc['store1']['Cost'])    # OK


##  Pandas的loc/iloc用来在保留index的情况下对DataFrame进行column上的操作
# pandas的column上一般会有一个名字，所以在选取上总是基于label的，而不想Series对象一样，总是基于容易混淆的方括号
# 类似于关系数据库的对列（column）的投影（projection）
# loc/iloc 返回的是DataFrame的副本，而不是view，所以会有点慢


# 删除DataFrame用Drop(), index或者row标签作为入参
# 参数inplace,如果设为true，就直接修改，而不是返回一个新的DataFrame
# 参数axis，表示要删除的。等于0，表示row，如果要删除column就改为1
# drop 返回的也是做完drop操作后的新DataFrame
print(df.drop('store1'))

# 第二种删除方法，直接使用index，使用del命令
# 立即生效，不会返回视图
#        Cost Item purchased
#store1  22.5       Dog Food
#store1   2.5   Kitty Litter
#store2   5.0      Bird Seed
copy_df = df.copy()
del copy_df['Name']
print(copy_df)


# 向DataFrame中添加一个列，
#        Cost Item purchased   Name Location
#store1  22.5       Dog Food  Chris     None
#store1   2.5   Kitty Litter  Kevyn     None
#store2   5.0      Bird Seed  Vinod     None
# 直接修改，不是返回副本
df['Location'] = None
print(df)

# 向DataFrame中添加一行,并增加name作为第二个索引
df = df.set_index([df.index, 'Name'])
df.index.names = ['Location', 'Name']
df = df.append(pd.Series(data={'Cost': 3.00, 'Item Purchased': 'Kitty Food'}, name=('Store 2', 'Kevyn')))
print(df)
#               Cost Item Purchased
#Location Name
#Store 1  Chris  22.5       Dog Food
#         Kevyn   2.5   Kitty Litter
#Store 2  Vinod   5.0      Bird Seed
#         Kevyn   3.0     Kitty Food


# 通过广播的方式来修改所有的cost值
df['Cost']=df['Cost']*0.8
print(df)

# 得到的view，修改会直接更新df
# 如果不想修改df，就要通过副本来修改，调用df.copy()先
costs = df['Cost']
costs += 2
print(df)


##对CSV文件的操作
# 解决列过多时，省略显示的问题
pd.set_option('display.max_columns', None)

# remove encoding='ANSI'
df = pd.read_csv('..\cfg\olympic.csv' )
#print(df)
#                    0            1     2     3     4      5             6     7     8     9     10     11    12    13    14              15
# 0               NaN  Summer Games  01 !  02 !  03 !  Total  Winter Games  01 !  02 !  03 !  Total  Games  01 !  02 !  03 !  Combined Total
# 1  Afghanistan(AFG)            14     0     0     2      2             0     0     0     0      0     14     0     0     2               2
# 2      Algeria(ALG)            13     5     4     8     17             3     0     0     0      0     16     5     4     8              17
# 3    Argentina(ARG)            24    21    25    28     74            19     0     0     0      0     43    21    25    28              74
# 4      Armenia(ARM)             6     2     6     6     14             7     0     0     0      0     13     2     6     6              14


# 我们可以使用index_col来指示哪一列是索引，也可以使用header参数来指示文件中的哪一行可以用来作为标签
# 重新导入输入，设置index_col=0，这是第一列。使用skiprows来设置列的标签，忽略第一行，从第二行开始读取
# remove encoding='ANSI',在家里需要加上这个，在公司不需要
df = pd.read_csv('..\cfg\olympic.csv', index_col=0, skiprows=1)
#print(df.head()) # 输出如下
#                NaN  Summer Games  01 !  02 !  03 !  Total  Winter Games  01 !.1  02 !.1  03 !.1  Total  Games  01 !.2  02 !.2  03 !.2  Combined Total
#   Afghanistan(AFG)            14     0     0     2      2             0       0       0       0      0     14       0       0       2               2
#       Algeria(ALG)            13     5     4     8     17             3       0       0       0      0     16       5       4       8              17
#     Argentina(ARG)            24    21    25    28     74            19       0       0       0      0     43      21      25      28              74
#      Armenia(ARM)              6     2     6     6     14             7       0       0       0      0     13       2       6       6              14

# 夏季金牌罪过的国家
print("Qutesion1：")
#.iloc[0].index())
df['Country'] = df.index
print((df.sort_values(by=['01 !'], ascending=False)).iloc[0]['Country'])

# 取夏季金牌和冬季金牌之间差最大的国家
df['Country'] = df.index
#df['different'] = df['01 !'] - df['01 !.1']
#df = df.sort_values(by=['different'], ascending=False)

# 当column中有相同的名字时，会在重复的名字后加‘.1’,后缀，如上显示的 01!.01  01!.02。 我们可以通过Pandas来修改
# Pandas把所有的column的名字保存在 .columns属性中
print(df.columns)
# Index(['Summer Games', '01 !', '02 !', '03 !', 'Total', 'Winter Games',
#        '01 !.1', '02 !.1', '03 !.1', 'Total.1', 'Games', '01 !.2', '02 !.2',
#        '03 !.2', 'Combined Total'],
#      dtype='object')

# 我们可以通过rename来对column改名
# inplace设为True，立即更新df，而不是返回副本
for col in df.columns:
    if col[:2] == '01':
        df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
    elif col[:2] == '02':
        df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
    elif col[:2] == '03':
        df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
#print(df.head()) # 输出如下
#                         Summer Games Gold Silver! Bronze! Total  Winter Games  \
# Afghanistan(AFG)                  14    0       0       2     2             0
# Algeria(ALG)                      13    5       4       8    17             3
# Argentina(ARG)                    24   21      25      28    74            19
# Armenia(ARM)                       6    2       6       6    14             7
# Australasia(ANZ) [ANZ]             2    3       4       5    12             0

#                        Gold.1  Silver.1  Bronze.1 Total.1  Games Gold.2  \
# Afghanistan(AFG)            0         0         0       0     14      0
# Algeria(ALG)                0         0         0       0     16      5
# Argentina(ARG)              0         0         0       0     43     21
# Armenia(ARM)                0         0         0       0     13      2
# Australasia(ANZ) [ANZ]      0         0         0       0      2      3

#                         Silver.2  Bronze.2 Combined Total
# Afghanistan(AFG)               0         2              2
# Algeria(ALG)                   4         8             17
# Argentina(ARG)                25        28             74
# Armenia(ARM)                   6         6             14
# Australasia(ANZ) [ANZ]         4         5             12


##################################################
#           Querying a DataFrame                 #
##################################################
# 布尔屏蔽 (boolean masking) 是numpy快速查询的核心
# 布尔屏蔽 可以是一维的series，也可以是二维的dataFrame，里面的值都是True或者False，用来覆盖在我们查询的数据解构上
# 任何对应True的元素都会进入到我们的结果里， False的则不会
# 这个强大的功能，应用极广，比如图像
#df = pd.read_csv('..\cfg\olympic.csv', encoding='ANSI')

# 我们想要取得在夏季奥运会上获得金牌的国家
# 教程上直接 df['Gold'] > 0, 但编译器提示int不能和str比较，所以就
a = df['Gold'] > str(0)
#print(a)
# Afghanistan(AFG)                      False
# Algeria(ALG)                           True
# Argentina(ARG)                         True
# Armenia(ARM)                           True
# Australasia(ANZ) [ANZ]                 True

# 把where函数把布尔屏蔽作为条件，将其应用到DataFrame或Series
# 并返回一个相同形状的新的DataFrame或Series
# 没有得过金牌的国家里面的数据就是NaN，
only_Gold = df.where(df['Gold']>str(0))
print('only Gold country:\n')
print(only_Gold.head())

#                        Summer Games Gold Silver Bronze Total  Winter Games  \
# Afghanistan(AFG)                 NaN  NaN    NaN    NaN   NaN           NaN
# Algeria(ALG)                    13.0    5      4      8    17           3.0
# Argentina(ARG)                  24.0   21     25     28    74          19.0
# Armenia(ARM)                     6.0    2      6      6    14           7.0
# Australasia(ANZ) [ANZ]           2.0    3      4      5    12           0.0
#
#                       Gold.1 Silver.1 Bronze.1 Total.1  Games Gold.2  \
# Afghanistan(AFG)          NaN      NaN      NaN     NaN    NaN    NaN
# Algeria(ALG)                0        0        0       0   16.0      5
# Argentina(ARG)              0        0        0       0   43.0     21
# Armenia(ARM)                0        0        0       0   13.0      2
# Australasia(ANZ) [ANZ]      0        0        0       0    2.0      3
#
#                        Silver.2 Bronze.2 Combined Total
# Afghanistan(AFG)            NaN      NaN            NaN
# Algeria(ALG)                  4        8             17
# Argentina(ARG)               25       28             74
# Armenia(ARM)                  6        6             14
# Australasia(ANZ) [ANZ]        4        5             12

# 大多数DataFrame内置的统计功能都忽略NaN值
# 统计得过金牌的国家总数，而不是金牌的总数
print('\n统计得过金牌的国家的金牌总数 only_Gold[\'Gold\'].count():')
print(only_Gold['Gold'].count())    # 109
print('\n统计得过所有国家的总数 df[\'Gold\'].count():')
print(df['Gold'].count())    # 153

# 如果想删除包含NaN的row，可以使用dropna()
print('\n删除包含NaN的国际 only_Gold.dropna():')
b = only_Gold.dropna()
print(b.head(3))
#                 Summer Games Gold Silver Bronze Total  Winter Games Gold.1  \
# Algeria(ALG)            13.0    5      4      8    17           3.0      0
# Argentina(ARG)          24.0   21     25     28    74          19.0      0
# Armenia(ARM)             6.0    2      6      6    14           7.0      0

#               Silver.1 Bronze.1 Total.1  Games Gold.2 Silver.2 Bronze.2  \
# Algeria(ALG)          0        0       0   16.0      5        4        8
# Argentina(ARG)        0        0       0   43.0     21       25       28
# Armenia(ARM)          0        0       0   13.0      2        6        6

#               Combined Total
# Algeria(ALG)               17
# Argentina(ARG)             74
# Armenia(ARM)               14



# Pandas允许索引运算元使用布尔屏蔽，而不是列名称列表
# 这样可以比较快的过滤和减少DataFrame，而且Pandas会自动过滤没有值的行
# (df.where(df['Gold']>str(0))).dropna() == df[df['Gold']>str(0)]
print('\n另一种使用布尔屏蔽的方式 df[df[\'Gold\']>str(0)]:')
c = df[df['Gold']>str(0)]
print(c.head(3))

# 对两个布尔屏蔽进行逻辑比较运算，得到的另一个布尔屏蔽
# 所以可以连接一堆的and/or来创建更复杂的查询
print(len(df[ (df['Gold']>str(10)) & (df['Gold']<str(15)) ]))

# 在冬季运动会得过金牌，但在夏季运动会没得过金牌
print("在冬季运动会得过金牌，但在夏季运动会没得过金牌: ")
print(df[(df['Gold.1']>str(0)) & (df['Gold']==str(0))])
#                                          Summer Games Gold Silver Bronze  \
# Liechtenstein(LIE)                                  17    0      0      0
# Olympic Athletes from Russia(OAR) [OAR]              0    0      0      0

#                                          Total  Winter Games Gold.1 Silver.1  \
# Liechtenstein(LIE)                           0            19      2        2
# Olympic Athletes from Russia(OAR) [OAR]      0             1      2        6

#                                          Bronze.1 Total.1  Games Gold.2  \
# Liechtenstein(LIE)                              6      10     36      2
# Olympic Athletes from Russia(OAR) [OAR]         9      17      1      2
#
#                                          Silver.2 Bronze.2 Combined Total
# Liechtenstein(LIE)                              2        6             10
# Olympic Athletes from Russia(OAR) [OAR]         6        9             17



#############################################################################
#                       Indexing DataFrame                                  #
#############################################################################

# 索引本质上就是行的标签，行对应轴0（axis=0）
# 我们可以用set_index来设定索引，但是这个是破坏性的，它不保留当前的索引
# 如果想保留当前索引，可以手动创建一个新的列，并将index属性拷贝到新列中
# 在olympic表中我们使用国家名作为index，但如果想以夏季金牌的数量作为index
# 我们需要把原来的作为index的国家名保存在新列 country里，然后用set_index,使用夏季金牌数作为index，来设置新索引
df['Country'] = df.index
df = df.set_index('Gold')
print("使用夏季金牌数作为index:")
print(df.head())
#       Summer Games Silver Bronze Total  Winter Games Gold.1 Silver.1 Bronze.1  \
# Gold
# 0               14      0      2     2             0      0        0        0
# 5               13      4      8    17             3      0        0        0
# 21              24     25     28    74            19      0        0        0
# 2                6      6      6    14             7      0        0        0
# 3                2      4      5    12             0      0        0        0

#      Total.1  Games Gold.2 Silver.2 Bronze.2 Combined Total  \
# Gold
# 0          0     14      0        0        2              2
# 5          0     16      5        4        8             17
# 21         0     43     21       25       28             74
# 2          0     13      2        6        6             14
# 3          0      2      3        4        5             12

#                     Country
#Gold
#0           Afghanistan(AFG)
#5               Algeria(ALG)
#21            Argentina(ARG)
#2               Armenia(ARM)
#3     Australasia(ANZ) [ANZ]

# 我们还可以用reset_index来去除索引，这个会把原来的index作为索引，并创建一个新的索引
df = df.reset_index()
print(df.head())
#  Gold  Summer Games Silver Bronze Total  Winter Games Gold.1 Silver.1  \
#0    0            14      0      2     2             0      0        0
#1    5            13      4      8    17             3      0        0
#2   21            24     25     28    74            19      0        0
#3    2             6      6      6    14             7      0        0
#4    3             2      4      5    12             0      0        0

#  Bronze.1 Total.1  Games Gold.2 Silver.2 Bronze.2 Combined Total  \
#0        0       0     14      0        0        2              2
#1        0       0     16      5        4        8             17
#2        0       0     43     21       25       28             74
#3        0       0     13      2        6        6             14
#4        0       0      2      3        4        5             12

#                  Country
#0        Afghanistan(AFG)
#1            Algeria(ALG)
#2          Argentina(ARG)
#3            Armenia(ARM)
#4  Australasia(ANZ) [ANZ]




