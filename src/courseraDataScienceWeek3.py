
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
'''
print(pd.merge(staff_df, student_df, how='inner', left_on=['First Name','Last Name'], right_on=['First Name','Last Name']))
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

'''
---------------------------   Group by   -----------------------------------------
groupby 接受一些列名，然后对DataFrame进行分组
比如，我们先加载人口普查数据，然后排除州级摘要，其SUMLEV是40  
'''

# 第一种方法，遍历
#df = census_df[census_df['SUMLEV']==50]
#for state in df['STNAME'].unique():
    # 求州的人口平均值
#    avg = np.average(df.where(df['STNAME']==state).dropna()['CENSUS2010POP'])
    #print('State: '+state+', ave:'+str(avg))

# 第二种方法，groupby
#for state, group in census_df.groupby(by='STNAME',axis=0):
#    avg = np.average(group['CENSUS2010POP'])
#    print('State: ' + state + ', ave:' + str(avg))


# 99%的时候groupby用在一列或者多列上，但还可以给groupby提供一个函数
# 把州名的按首字母来分组，A~L的为0， M~P的为1，Q~Z为2，把这个规则作为groupby的分组规则
# 首先要先设置索引
df = census_df.set_index('STNAME')
def fun(item):
    if item[0] < 'M':
        return 0
    elif item[0] < 'Q':
        return 1
    else:
        return 2

# 这里groupby会把已经设置好的索引STNAME作为入参传给fun()
#for group, frame in df.groupby(fun):
    #print('There are ' + str(len(frame))+' in group '+ str(group) +' to processing')
'''
There are 1196 in group 0 to processing
There are 1154 in group 1 to processing
There are 843 in group 2 to processing
'''

# groupby的常用功能就是分割数据
# 这被称为分割split，应用apply和组合combine模式
# groupby的agg应用方法，就是聚合aggregate
df = census_df[census_df['SUMLEV']==50]
# groupby是分割，agg是应用，应用的对象是'CENSUS2010POP'，所作的操作是np.average方法
#print(df.groupby('STNAME').agg({'CENSUS2010POP':np.average}))


#-------------------------
# 一个表有Category，Quantity，Weight (oz.)
# 要对Category分组，求Quantity*Weight 的值

#print(df.groupby('Category').apply(lambda df,a,b: sum(df[a] * df[b]), 'Weight (oz.)', 'Quantity'))

# Or alternatively without using a lambda:
# def totalweight(df, w, q):
#        return sum(df[w] * df[q])
#
# print(df.groupby('Category').apply(totalweight, 'Weight (oz.)', 'Quantity'))


'''
当你传入的字典，它既可以用来识别你要应用函数的列，或如果有多个函数要应用的话，可以应用在命名输出的列，
差别在于你传入的字典的键和他的命名方式

groupby对象其实有两个，DataFrameGroupBy和SeriesGroupBy对象
他们的不同之处在于，当使用agg时，
'''
#print(type(df.groupby(level=0)['POPESTIMATE2010','POPESTIMATE2011']))
#print(type(df.groupby(level=0)['POPESTIMATE2010']))
#<class 'pandas.core.groupby.groupby.DataFrameGroupBy'>
#<class 'pandas.core.groupby.groupby.SeriesGroupBy'>



'''
对人口普查数据，将其转换为以州名称，为索引，只用列CENSUS2010POP作为数据
'''
#print(df.set_index('STNAME').groupby(level=0)['CENSUS2010POP'].agg({'avg':np.average, 'sum':np.sum, 'max':np.max}))

'''
我们也可以通过使用DataFrame来做这件事
下面这个例子，传递给agg的字典的key，会以这个key创建一个分层标记的列
'''
#print(df.set_index('STNAME').groupby(level=0)['POPESTIMATE2010','POPESTIMATE2011'].agg({'avg':np.average, 'sum':np.sum}).head(3))
'''
                    sum                             avg
        POPESTIMATE2010 POPESTIMATE2011 POPESTIMATE2010 POPESTIMATE2011
STNAME
Alabama         4785161         4801108    71420.313433    71658.328358
Alaska           714021          722720    24621.413793    24921.379310
Arizona         6408208         6468732   427213.866667   431248.800000
'''

'''
我们也可以通过使用DataFrame来做这件事
下面这个例子，与上面的不同，传递给agg的字典的key就是原dataframe的列名，而不会创建分层标记的列
这种方式用的比较少
'''
#print(df.set_index('STNAME').groupby(level=0)['POPESTIMATE2010','POPESTIMATE2011'].agg({'POPESTIMATE2010':np.average, 'POPESTIMATE2011':np.sum}).head(3))
'''
         POPESTIMATE2010  POPESTIMATE2011
STNAME
Alabama     71420.313433          4801108
Alaska      24621.413793           722720
Arizona    427213.866667          6468732
'''



'''
----------------------         Scales          --------------------------
'''

'''
作为一个数据科学家，有四个尺度需要了解：
1. 比率尺度。ratio，在比率尺度中，单位间隔相等。数学运算，加减乘除，都有效。比如，高度和重量
2. 间隔尺度。Interval，单位间隔相等，没有一个真正的零，所以乘法和除法是无效的。比如 温度
3. 序数尺度。Ordinal，在序数尺度，值的顺序很重要，但值之间的差异不等间隔，
4. 名义尺度。nominal，在Pandas里一般被称为分类（categorical）数据，
数据挖掘所做的大部分工作里，比率尺度和间隔尺度的差异不是那么大

尺度的重要性就在于在统计和机器学习方面，Pandas有很多有趣的功能在不同的测量测度之间转换，
'''

'''
Pandas有内置的分类数据，你可以使用astype方法将column设置为分类数据
astype方法会把你的数据设置为分类数据，astype会更改你的数据的底层类型。
你也可以进一步将其更改为序数数据，通过将ordered标志设为True，并以有序的方式传递分类
'''
df = pd.DataFrame(['A+', 'A', 'A-', 'B+', 'B', 'B-', 'C+', 'C', 'C-', 'D+', 'D'],
                  index=['excellent', 'excellent', 'excellent', 'good', 'good', 'good', 'ok', 'ok', 'ok', 'poor', 'poor'])

df.rename(columns={0: 'Grades'}, inplace=True)
'''
          Grades
excellent     A+
excellent      A
excellent     A-
good          B+
good           B
good          B-
ok            C+
ok             C
ok            C-
poor          D+
poor           D
'''

''''
我们指示Pandas将其作为分类数据时，dtype已经是category，并且有了11个不同的类别
'''
#print(df['Grades'].astype('category').head())
'''
excellent    A+
excellent     A
excellent    A-
good         B+
good          B
Name: Grades, dtype: category
Categories (11, object): [A, A+, A-, B, ..., C+, C-, D, D+]
'''

'''
如果我们想要想Pandas表明这些数据是按逻辑顺序的，我们可以设置ordered=True，
'''
#grades = df['Grades'].astype('category',
#                             categories=['D', 'D+', 'C-', 'C', 'C+', 'B-', 'B', 'B+', 'A-', 'A', 'A+'],
#                             ordered=True)
#print(grades)
'''
Name: Grades, dtype: category
Categories (11, object): [D < D+ < C- < C ... B+ < A- < A < A+]
'''
#print(grades > 'C')
'''
excellent     True
excellent     True
excellent     True
good          True
good          True
good          True
ok            True
ok           False
ok           False
poor         False
poor         False
Name: Grades, dtype: bool
'''

'''
序数数据有一个排序，它可以帮助你进行布尔屏蔽，
比如，我们有我们的成绩列表，我们将它与C比较，如果根据字典顺序，C+和C-都大于C，可是我们已经了数据顺序
然后我们可以
'''


'''
如果我们使用机器学习分类方法处理数据，则需要使用分类数据，所以降低维度dimensionality也是有用的。
Pandas的Cut功能，它接受一个参数，这个参数可以是一个Series或DataFrame。它还需要使用多个盒子bins
并且所有盒子保持相同间距，

'''
#df.groupby(level=0)['CENSUS2010POP'].agg({'ave':np.average})
#print(pd.cut(df['avg'],10))

ages = [20, 22, 25, 27, 21, 23, 37, 31, 61, 45, 41, 32]
bins = [18, 25, 35, 60, 100]    # bins可以是整数，表示划分为几份，也可以是这样的数组，表示按照这几个节点划分
cats = pd.cut(ages, bins, labels=['s', 'm', 'l', 'xl'])
#print(cats)
'''
[s, s, s, m, s, ..., m, xl, l, l, m]
Length: 12
Categories (4, object): [s < m < l < xl]
'''
#print(cats.codes)
'''
[0 0 0 1 0 0 2 1 3 2 2 1]
表示12个元素分别处于4个区间的哪一个
'''
#print(cats.categories)
#Index(['s', 'm', 'l', 'xl'], dtype='object')
#print(pd.value_counts(cats))
'''
s     5
l     3
m     3
xl    1
dtype: int64
'''

data = np.random.rand(20)
'''
[0.70081209 0.37097134 0.6662884  0.0961317  0.02201284 0.58679348
 0.35126993 0.82245626 0.44544119 0.49660155 0.98868394 0.98236028
 0.13529538 0.26003261 0.90252838 0.18780304 0.39163854 0.80016992
 0.59936142 0.66380607]
'''
#print(data)
#print(pd.cut(data, 5, precision=2))
'''
[(0.6, 0.8], (0.22, 0.41], (0.6, 0.8], (0.021, 0.22], (0.021, 0.22], ..., (0.021, 0.22], (0.22, 0.41], (0.8, 0.99], (0.41, 0.6], (0.6, 0.8]]
Length: 20
Categories (5, interval[float64]): [(0.021, 0.22] < (0.22, 0.41] < (0.41, 0.6] < (0.6, 0.8] <
                                    (0.8, 0.99]]
precision指定精度，
'''


'''
------------------------   Pivot Table   ------------------------------
枢纽分析表，又称为透视表，为了特定的目的，聚合DataFrame中的数据的一种方式
它大量使用聚合agg功能，Pivot Table本身就是一个DataFrame，其中行代表一个变数

'''
pd.set_option('display.width', 500)
df = pd.read_csv('..\cfg\cars.csv', encoding='gbk')
#print(df.head())
'''
   YEAR        MAKE           MODEL        SIZE   (kW) Unnamed:5 TYPE  CITY (kWh/100 km)  HWY (kWh/100 km)  COMB (kWh/100 km)  CITY (Le/100 km)  HWY (Le/100 km)  COMB (Le/100 km)  (g/km)  RATING  RATING.1   (km)  TIME (h)
0  2012  MITSUBISHI          i-MiEV  SUBCOMPACT   49.0        A1    B               16.9              21.4               18.7               1.9              2.4               2.1     0.0     NaN       NaN  100.0       7.0
1  2012      NISSAN            LEAF    MID-SIZE   80.0        A1    B               19.3              23.0               21.1               2.2              2.6               2.4     0.0     NaN       NaN  117.0       7.0
2  2013        FORD  FOCUS ELECTRIC     COMPACT  107.0        A1    B               19.0              21.1               20.0               2.1              2.4               2.2     0.0     NaN       NaN  122.0       4.0
3  2013  MITSUBISHI          i-MiEV  SUBCOMPACT   49.0        A1    B               16.9              21.4               18.7               1.9              2.4               2.1     0.0     NaN       NaN  100.0       7.0
4  2013      NISSAN            LEAF    MID-SIZE   80.0        A1    B               19.3              23.0               21.1               2.2              2.6               2.4     0.0     NaN       NaN  117.0       7.0

'''
#print(df.pivot_table(index=['YEAR'], values=['(kW)'], columns=['MAKE'], aggfunc=np.mean))
'''
这句透视表的作用的就是，YEAR作为row（index）， MAKE作为column，kw作为数据，并对kw的数据求平均 np.mean
没有值的，就用NaN
      (kW)
MAKE    BMW CHEVROLET   FORD HYUNDAI   KIA MITSUBISHI NISSAN SMART       TESLA TESLA  VOLKSWAGEN
YEAR
2012    NaN       NaN    NaN     NaN   NaN       49.0   80.0   NaN         NaN    NaN        NaN
2013    NaN       NaN  107.0     NaN   NaN       49.0   80.0  35.0  257.500000    NaN        NaN
2014    NaN     104.0  107.0     NaN   NaN       49.0   80.0  35.0  268.333333    NaN        NaN
2015  125.0     104.0  107.0     NaN  81.0       49.0   80.0  35.0  321.666667    NaN        NaN
2016  125.0     104.0  107.0     NaN  81.0       49.0   80.0  35.0  409.823529  386.0        NaN
2017  125.0     150.0  107.0    88.0  81.0       49.0   80.0   NaN  383.142857  464.0      100.0
2018  130.0     150.0  107.0    88.0  81.0        NaN  110.0  60.0  387.300000    NaN      100.0
'''

'''
如果我们希望针对同一个透视表，进行不同的操作，比如同时显示sum和mean，则可以添加margins=True来显示
现在每个功能都有一个all类别，它在给定的年份和厂家上，显示总体平均值和最小值，
如果margins为False则不显示all
'''
#print(df.pivot_table(index=['YEAR'], values=['(kW)'], columns=['MAKE'], aggfunc=[np.mean,np.min], margins=False))
'''
            mean                                                                                                      amin
            (kW)                                                                                                      (kW)
MAKE         BMW CHEVROLET   FORD HYUNDAI   KIA MITSUBISHI  NISSAN SMART       TESLA  TESLA  VOLKSWAGEN         All    BMW CHEVROLET   FORD HYUNDAI   KIA MITSUBISHI NISSAN SMART  TESLA TESLA  VOLKSWAGEN   All
YEAR
2012         NaN       NaN    NaN     NaN   NaN       49.0   80.00   NaN         NaN     NaN        NaN   64.500000    NaN       NaN    NaN     NaN   NaN       49.0   80.0   NaN    NaN    NaN        NaN  49.0
2013         NaN       NaN  107.0     NaN   NaN       49.0   80.00  35.0  257.500000     NaN        NaN  148.444444    NaN       NaN  107.0     NaN   NaN       49.0   80.0  35.0  225.0    NaN        NaN  35.0
2014         NaN     104.0  107.0     NaN   NaN       49.0   80.00  35.0  268.333333     NaN        NaN  135.000000    NaN     104.0  107.0     NaN   NaN       49.0   80.0  35.0  225.0    NaN        NaN  35.0
2015  125.000000     104.0  107.0     NaN  81.0       49.0   80.00  35.0  321.666667     NaN        NaN  181.857143  125.0     104.0  107.0     NaN  81.0       49.0   80.0  35.0  280.0    NaN        NaN  35.0
2016  125.000000     104.0  107.0     NaN  81.0       49.0   80.00  35.0  409.823529  386.00        NaN  298.111111  125.0     104.0  107.0     NaN  81.0       49.0   80.0  35.0  285.0  386.0        NaN  35.0
2017  125.000000     150.0  107.0    88.0  81.0       49.0   80.00   NaN  383.142857  464.00      100.0  297.173913  125.0     150.0  107.0    88.0  81.0       49.0   80.0   NaN  285.0  386.0      100.0  49.0
2018  130.000000     150.0  107.0    88.0  81.0        NaN  110.00  60.0  387.300000     NaN      100.0  244.450000  125.0     150.0  107.0    88.0  81.0        NaN  110.0  60.0  192.0    NaN      100.0  60.0
All   126.666667     122.4  107.0    88.0  81.0       49.0   83.75  40.0  367.808511  454.25      100.0  240.375000  125.0     104.0  107.0    88.0  81.0       49.0   80.0  35.0  192.0  386.0      100.0  35.0

'''


'''
-----------------------------           在Pandas中查看时间序列是日期           -------------------------------------
'''
'''
Pandas有四种与时间相关的类型：Timestamp, DatetimeIndex, Period和PeriodIndex
Timestamp：单个时间戳，并将值和时间点相关联，大多数情况下Timestamp可以于Python的datatime互换
'''
#print(pd.Timestamp('11/9/2018 16:10'))
#2018-11-09 16:10:00

'''
Period表示单个时间跨度，例如特定的日期或者月份
'''
#print(pd.Period('11/2018'))
# 2018-11
#print(pd.Period('11/9/2018'))
# 2018-11-09

'''
timestamp的索引index是DatetimeIndex
下面的例子，每个timestamp作为索引，查看索引的类型为DatetimeIndex
'''
t1 = pd.Series(list('abc'),[pd.Timestamp('2018-11-5'), pd.Timestamp('2018-11-6'), pd.Timestamp('2018-11-7')])
#print(t1)
#print(t1.index)
'''
2018-11-05    a
2018-11-06    b
2018-11-07    c
dtype: object

DatetimeIndex(['2018-11-05', '2018-11-06', '2018-11-07'], dtype='datetime64[ns]', freq=None)
'''

'''
同样Period的索引是PeriodIndex
'''

t2 = pd.Series(list('def'),[pd.Period('2018-11-5'), pd.Period('2018-11-6'), pd.Period('2018-11-7')])
#print(t2)
#print(t2.index)
'''
2018-11-05    d
2018-11-06    e
2018-11-07    f
Freq: D, dtype: object
PeriodIndex(['2018-11-05', '2018-11-06', '2018-11-07'], dtype='period[D]', freq='D')
'''


'''
转换日期时间
'''
d1 = ['2 June 2013', 'Aug 29, 2014', '2015-06-26', '7/12/16']
ts3 = pd.DataFrame(np.random.randint(10,100,(4,2)),index=d1, columns=list('ab'))
#print(ts3)
'''
               a   b
2 June 2013   77  76
Aug 29, 2014  75  41
2015-06-26    29  10
7/12/16       97  15

这里index的日期格式很混乱，使用to_datetime，pandas会尝试转化为日期时间，并放到标准格式中
'''
ts3.index = pd.to_datetime(ts3.index)
#print(ts3)
'''
             a   b
2013-06-02  29  10
2014-08-29  46  93
2015-06-26  57  66
2016-07-12  29  53

to_datetime还有更改日期解析顺序的选项， dayfirst=True来解析欧洲日期格式
'''
#print(pd.to_datetime('4.7.12', dayfirst=True))
#2012-07-04 00:00:00


'''
时间差 Timedelta
两个时间戳的间隔
'''
#print(pd.Timestamp('11/9/2018') - pd.Timestamp('1/6/2011'))
#print(type(pd.Timestamp('11/9/2018') - pd.Timestamp('1/6/2011')))
'''
2864 days 00:00:00
<class 'pandas._libs.tslibs.timedeltas.Timedelta'>
'''

'''
也可以在一个Timestamp的基础上加一个Timedelta
'''
#print(pd.Timestamp('11/9/2018') + pd.Timedelta(weeks=2,days=10,hours=12,minutes=2.4,seconds=10.3))
'''
2018-12-03 12:02:34.300000
'''


'''
查看九次测量，两周一次，每个周日，从2016年10月开始，使用data_range，我们可以创建这个DatetimeIndex
pandas.date_range(start=None, end=None, periods=None, freq='D', tz=None, normalize=False, name=None, closed=None, **kwargs)
freq='M'每月，'3M'3个月，
'''
dates = pd.date_range('10-01-2016', periods=9, freq='2w-SUN')
#print(dates)
'''
DatetimeIndex(['2016-10-02', '2016-10-16', '2016-10-30', '2016-11-13', '2016-11-27', '2016-12-11', '2016-12-25', '2017-01-08', '2017-01-22'], dtype='datetime64[ns]', freq='2W-SUN')
'''

'''
使用日期和随机数
'''
df = pd.DataFrame( {'Count1 ':100+np.random.randint(-5, 10, 9).cumsum(), 'Count2':120+np.random.randint(-5, 10, 9)}, index=dates)
#print(df)
'''

            Count1   Count2
2016-10-02       97     119
2016-10-16      101     115
2016-10-30      106     118
2016-11-13      112     118
2016-11-27      115     115
2016-12-11      118     124
2016-12-25      123     118
2017-01-08      120     129
2017-01-22      123     115
'''

#print(df.index.weekday_name)
'''
Index(['Sunday', 'Sunday', 'Sunday', 'Sunday', 'Sunday', 'Sunday', 'Sunday', 'Sunday', 'Sunday'], dtype='object')
'''

'''
使用diff来查找每个日期值之间的差异
'''
#print(df.diff())
'''
            Count1   Count2
2016-10-02      NaN     NaN
2016-10-16      0.0    -1.0
2016-10-30      4.0    -3.0
2016-11-13     -5.0     6.0
2016-11-27      4.0    -2.0
2016-12-11      4.0     3.0
2016-12-25     -5.0    -3.0
2017-01-08      2.0    -1.0
2017-01-22      3.0     1.0
'''


'''
如果想知道每个月的平均数
'''
#print(df.resample('M').mean())
'''
            Count1       Count2
2016-10-31    105.0  124.666667
2016-11-30    110.0  121.500000
2016-12-31    115.5  125.500000
2017-01-31    108.0  124.000000
'''

'''
使用部分字符串索引来查询特定年份
'''
#print(df['2017'])
'''
            Count1   Count2
2017-01-08      151     127
2017-01-22      146     120
'''

'''
使用部分字符串索引来查询特定月份
'''
#print(df['2016-12'])
'''
            Count1   Count2
2016-12-11      111     123
2016-12-25      111     120
'''

'''
对时间进行切片
'''
print(df['2016-12':])
'''
            Count1   Count2
2016-12-11      120     120
2016-12-25      129     124
2017-01-08      124     117
2017-01-22      128     125
'''

'''
可以在DataFrame中更改我们日期的频率，使用asfreq
把之前的频率从每两周改为每周，我们每隔一周就会丢失值，所以我们队这些丢失的值使用正向填充ffill方法
'''
print(df.asfreq('W', method='ffill'))
'''
            Count1   Count2
2016-10-02      109     122
2016-10-09      109     122
2016-10-16      113     125
2016-10-23      113     125
2016-10-30      114     115
2016-11-06      114     115
2016-11-13      112     127
2016-11-20      112     127
2016-11-27      107     122
2016-12-04      107     122
2016-12-11      114     121
2016-12-18      114     121
2016-12-25      119     117
2017-01-01      119     117
2017-01-08      119     116
2017-01-15      119     116
2017-01-22      115     119
'''


'''
绘制时间序列
'''
