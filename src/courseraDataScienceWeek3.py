
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
 1. 我们想要所有人的名单及详细信息，在数据库中，这称为full outer join，在集合理论中，称为union
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