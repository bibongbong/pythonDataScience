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

# 通过广播的方式来修改所有的cost值
df['Cost']=df['Cost']*0.8
print(df)

# 得到的view，修改会直接更新df
# 如果不想修改df，就要通过副本来修改，调用df.copy()先
costs = df['Cost']
costs += 2
print(df)


##对CSV文件的操作
df = pd.read_csv('..\cfg\mysameple.csv')
print(df)
#             0                   1      ...                   8              9
#0  SRM_SaaS_ES  MXPERUSERInterface      ...                   d              d
#1      LOGINID            PERSONID      ...        ADDRESSLINE3  BILLTOADDRESS
#2     manoel11            manoel11      ...                   e  BILLTOADDRES
#[3 rows x 10 columns]

# 我们可以使用index_col来指示哪一列是索引，也可以使用header参数来指示文件中的哪一行可以用来作为标签
# 重新导入输入，设置index_col=0，这是第一列。使用skiprows来设置列的标签，忽略第一行，从第二行开始读取
df = pd.read_csv('..\cfg\mysameple.csv', index_col=0, skiprows=1)
print(df)
#            MXPERUSERInterface      ...                  d.5
#SRM_SaaS_ES                         ...
#LOGINID               PERSONID      ...        BILLTOADDRESS
#manoel11              manoel11      ...        BILLTOADDRESS
