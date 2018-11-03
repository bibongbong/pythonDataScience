
'''
 对一维的Series和二维的DataFrame有多种不同的访问和查询方式
 比如，使用iloc和loc属性进行行查询，或者使用方括号进行列查询，以及布尔屏蔽
 布尔屏蔽非常强大，它允许我们使用广播来确定我们在分析中应该保留哪些数据。比如week2的第八题

 Week3学习内容
    1. Groupby和Apply来减少和处理数据
    2. 如何将多个文件的数据集合在一起
    3. Pandas中对于传统统计分析和机器学习的功能
'''

'''
----------------   合并数据集    --------------------
我们只需要将带有新列名称的方括号运算符，只要索引共用，数据就被添加了
如果没有共享索引，并且传入一个标量值 scalar value，这个标量值只是一个整数或一个字符串，添加在列的新值，是以纯量scalar value作为预设值

如何为每一行分配一个不同的值呢？
'''
import pandas as pd

df = pd.DataFrame([{'Name': 'Chris', 'Item Purchased': 'Sponge', 'Cost': 22.50},
                   {'Name': 'Kevyn', 'Item Purchased': 'Kitty Litter', 'Cost': 2.50},
                   {'Name': 'Filip', 'Item Purchased': 'Spoon', 'Cost': 5.00}],
                  index=['Store 1', 'Store 1', 'Store 2'])

# 添加一个Date列，并为每一行设定一个这个列的值
df['Date'] = ['December 1', 'January 1', 'mid-May']
'''
print(df)
         Cost Item Purchased   Name        Date
Store 1  22.5         Sponge  Chris  December 1
Store 1   2.5   Kitty Litter  Kevyn   January 1
Store 2   5.0          Spoon  Filip     mid-May

'''

# 也可以设定一个默认值
df['Delivered'] = True
'''
print(df)
         Cost Item Purchased   Name        Date  Delivered
Store 1  22.5         Sponge  Chris  December 1       True
Store 1   2.5   Kitty Litter  Kevyn   January 1       True
Store 2   5.0          Spoon  Filip     mid-May       True

'''


# 或者设定若干个有效值，其他的置空
df['Feedback'] = ['Positive', None, 'Negative']
'''
print(df)
         Cost Item Purchased   Name        Date  Delivered  Feedback
Store 1  22.5         Sponge  Chris  December 1       True  Positive
Store 1   2.5   Kitty Litter  Kevyn   January 1       True      None
Store 2   5.0          Spoon  Filip     mid-May       True  Negative

'''

# 先resetIndex，再使用index(0..2)来指定某行的值，没有指定的行则为NaN
# 这是非常好的方法去指定某些行的值
adf = df.reset_index()
adf['Date'] = pd.Series({0: 'December 1', 2: 'mid-May'})
'''
print(adf)
     index  Cost Item Purchased    ...           Date Delivered  Feedback
0  Store 1  22.5         Sponge    ...     December 1      True  Positive
1  Store 1   2.5   Kitty Litter    ...            NaN      True      None
2  Store 2   5.0          Spoon    ...        mid-May      True  Negative

'''



'''
 更常见的是，我们希望结合两个比较大的DataFrame在一起，首先我们需要解决一些关联理论，并设定一些语言惯例
 Venn图，用来显示集合的关系。设定两个dataframe，学生和雇员，有的人既是学生又是雇员。比如我们可以把人名作为index
 当我们想结合这两个DataFrame时，比如
 1. 我们想要所有人的名单及详细信息，在数据库中，这称为full outer join，在集合理论中，称为合并union
 2. 得到既是学生又是雇员的人的名单，数据库中称为内连接，inner join， 集合中称为交集 intersection

 这就需要用到Pandas的Merge功能
'''

staff_df = pd.DataFrame([{'Name': 'Kelly', 'Role': 'Director of HR'},
                         {'Name': 'Sally', 'Role': 'Course liasion'},
                         {'Name': 'James', 'Role': 'Grader'}])
staff_df = staff_df.set_index('Name')
student_df = pd.DataFrame([{'Name': 'James', 'School': 'Business'},
                           {'Name': 'Mike', 'School': 'Law'},
                           {'Name': 'Sally', 'School': 'Engineering'}])
student_df = student_df.set_index('Name')
'''
print(staff_df)
                 Role
Name
Kelly  Director of HR
Sally  Course liasion
James          Grader


print(student_df)
            School
Name
James     Business
Mike           Law
Sally  Engineering

'''

# 把两个DataFrame进行合并，第三个参数是要进行的操作外连接，也就是求并集，并且用左索引和右索引作为结合列
# James和Sally既是职员又是学生，他们在各自表中的行合并为一行
opd = pd.merge(staff_df,student_df, how='outer', left_index=True, right_index=True)

'''
print(opd)
                 Role       School
Name                              
James          Grader     Business
Kelly  Director of HR          NaN
Mike              NaN          Law
Sally  Course liasion  Engineering
'''


# 如果要求交集，也就是intersection，how属性设为inner 内连接
ipd = pd.merge(staff_df,student_df,how='inner', left_index=True, right_index=True)
'''
print(ipd)
                 Role       School
Name                              
Sally  Course liasion  Engineering
James          Grader     Business
'''


# 集合加法
# 当我们想要所有员工的名单，不论他们是否学生。但如果他们是学生，我们也想要获得他们的学生信息
# 相当于以staff_df为基础，同时用student_df补充其内容
# Kelly不是学生，所以在School里没有其信息
lpd = pd.merge(staff_df,student_df, how='left', left_index=True, right_index=True)
#print(lpd)
'''
                 Role       School
Name                              
Kelly  Director of HR          NaN
Sally  Course liasion  Engineering
James          Grader     Business
'''

# 同理，右连接，以student_df为基础，获得所有学生的信息，如果他们还是员工，则也获得他们的员工信息
# Mike不是员工所以Role里没有其信息
rpd = pd.merge(staff_df, student_df, how='right', left_index=True, right_index=True)
'''
print(rpd)
                 Role       School
Name                              
James          Grader     Business
Mike              NaN          Law
Sally  Course liasion  Engineering
'''

# 另外还可以不使用index，可以使用列来代替index
# 下例，还是左连接，以‘Name’作为index
staff_df = staff_df.reset_index()
student_df = student_df.reset_index()
lopd = pd.merge(staff_df, student_df, how='left', left_on='Name', right_on='Name')
'''
print(lopd)
    Name            Role       School
0  Kelly  Director of HR          NaN
1  Sally  Course liasion  Engineering
2  James          Grader     Business
'''


# 当DataFrame之间有冲突时怎么处理
# 下例，James和Sally 在两个表里的location的值不同，merge时把两个Location列分别命名为Location_x和Location_y
# index，也就是'Name'左边的属于staff_df的Location，右边的是student_df的Location
staff_df = pd.DataFrame([{'Name': 'Kelly', 'Role': 'Director of HR', 'Location': 'State Street'},
                         {'Name': 'Sally', 'Role': 'Course liasion', 'Location': 'Washington Avenue'},
                         {'Name': 'James', 'Role': 'Grader', 'Location': 'Washington Avenue'}])
student_df = pd.DataFrame([{'Name': 'James', 'School': 'Business', 'Location': '1024 Billiard Avenue'},
                           {'Name': 'Mike', 'School': 'Law', 'Location': 'Fraternity House #22'},
                           {'Name': 'Sally', 'School': 'Engineering', 'Location': '512 Wilson Crescent'}])
conf_pd = pd.merge(staff_df, student_df, how='left', left_on='Name', right_on='Name')
pd.set_option('display.max_columns', None)

'''
print(conf_pd)
          Location_x   Name            Role            Location_y       School
0       State Street  Kelly  Director of HR                   NaN          NaN
1  Washington Avenue  Sally  Course liasion   512 Wilson Crescent  Engineering
2  Washington Avenue  James          Grader  1024 Billiard Avenue     Business
'''


'''
多索引和多列
名字可能相同，但姓相同的少，比如James Wilde和James Hammond，我们设置'FirstName'和‘LastName’两类，
不管是使用left_on还是right_on，在使用inner连接，就是求交集时都找不到这些人

'''
staff_df = pd.DataFrame([{'First Name': 'Kelly', 'Last Name': 'Desjardins', 'Role': 'Director of HR'},
                         {'First Name': 'Sally', 'Last Name': 'Brooks', 'Role': 'Course liasion'},
                         {'First Name': 'James', 'Last Name': 'Wilde', 'Role': 'Grader'}])
student_df = pd.DataFrame([{'First Name': 'James', 'Last Name': 'Hammond', 'School': 'Business'},
                           {'First Name': 'Mike', 'Last Name': 'Smith', 'School': 'Law'},
                           {'First Name': 'Sally', 'Last Name': 'Brooks', 'School': 'Engineering'}])
staff_df
student_df
print(pd.merge(staff_df, student_df, how='inner', left_on=['First Name','Last Name'], right_on=['First Name','Last Name']))
'''
  First Name Last Name            Role       School
0      Sally    Brooks  Course liasion  Engineering
'''

'''
---------------------------   Pandas Idioms   -----------------------------------------
idoms惯用的意思

例如，你想取名为Washtenaw的县的总人口，df.loc['Washtenaw']['Total Population']，这通常是个很糟糕的做法，它会返回DataFrame的副本
经验法则：如果你看到一个背靠背的方括号 '][',你就该好好思考一下了。
    
惯用的解决方案通常具有高性能和高可读性。例如尽可能使用向量化， 尽量避免反复使用loops。我们把这些称为pandorable
1. 方法连接 method chaining。当查询DataFrame时，可以将pandas的程序调用链接在一起
    对某个对象使用每个方法，都会返回对该对象的引用，这样的好处是可以将不同的操作应用在一个DataFrame，集中在一行或至少一个语句中

以下是同一种功能的两种实现

(df.where(df['SUMLEV']==50)
    .dropna()
    .set_index(['STNAME','CTYNAME'])
    .rename(columns={'ESTIMATESBASE2010': 'Estimates Base 2010'}))

df = df[df['SUMLEV']==50]
df.set_index(['STNAME','CTYNAME'], inplace=True)
df.rename(columns={'ESTIMATESBASE2010': 'Estimates Base 2010'})
'''

'''
另一个惯用法：
Python的Map功能，使用Map时，传递一些你想要调用的函数，一些可迭代的对象。
在Pandas中有apply，它提供了对DataFrame的每个单元格进行操作的函数。applymap很好，但是很少使用
统计中，有五列对应一年的估计，我们可以创建一个新列min或者max
'''
census_df = pd.read_csv('..\cfg\co-est2015-alldata.csv', encoding='gbk')
import numpy as np
def min_max(row):
    #取某列，要用到双方括号[[]]
    columns = row[['POPESTIMATE2010',
                'POPESTIMATE2011',
                'POPESTIMATE2012',
                'POPESTIMATE2013',
                'POPESTIMATE2014',
                'POPESTIMATE2015']]
    # 生成一个新的Series
    return pd.Series({'min':np.min(columns), 'max':np.max(columns)})

# 一般axis=0表示对行进行操作，比如b.sum(axis=0)，对b的每行的值做sum，行总数，
# b.sum(axis=1)，对b的每行的值做sum，列总数
# 但在这里，要应用到所有的行，axis必须等于1
#print(.apply(min_max, axis=1))

# 如果是要在原来的DataFrame的基础上添加Min Max列。
# row['min'] = np.min(data)
# row['max'] = np.max(data)

# 可以使用lambda
rows = ['POPESTIMATE2010',
        'POPESTIMATE2011',
        'POPESTIMATE2012',
        'POPESTIMATE2013',
        'POPESTIMATE2014',
        'POPESTIMATE2015']
census_df.apply(lambda x:np.max(x[rows]), axis=1)
