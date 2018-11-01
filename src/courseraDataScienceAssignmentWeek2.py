# coding: utf-8

# ---
#
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
#
# ---

# # Assignment 2 - Pandas Introduction
# All questions are weighted the same in this assignment.
# ## Part 1
# The following code loads the olympics dataset (olympics.csv), which was derrived from the Wikipedia entry on [All Time Olympic Games Medals](https://en.wikipedia.org/wiki/All-time_Olympic_Games_medal_table), and does some basic data cleaning.
#
# The columns are organized as # of Summer games, Summer medals, # of Winter games, Winter medals, total # number of games, total # of medals. Use this dataset to answer the questions below.

# In[ ]:

import pandas as pd

df = pd.read_csv('olympics.csv', index_col=0, skiprows=1)

for col in df.columns:
	if col[:2]=='01':
		df.rename(columns={col:'Gold'+col[4:]}, inplace=True)
	if col[:2]=='02':
		df.rename(columns={col:'Silver'+col[4:]}, inplace=True)
	if col[:2]=='03':
		df.rename(columns={col:'Bronze'+col[4:]}, inplace=True)
	if col[:1]=='№':
		df.rename(columns={col:'#'+col[1:]}, inplace=True)

names_ids = df.index.str.split('\s\(') # split the index by '('

df.index = names_ids.str[0] # the [0] element is the country name (new index)
df['ID'] = names_ids.str[1].str[:3] # the [1] element is the abbreviation or ID (take first 3 characters from that)

df = df.drop('Totals')
df.head()


# ### Question 0 (Example)
#
# What is the first country in df?
#
# *This function should return a Series.*

# In[ ]:

# You should write your whole answer within the function provided. The autograder will call
# this function and compare the return value against the correct solution value
def answer_zero():
	# This function returns the row for Afghanistan, which is a Series object. The assignment
	# question description will tell you the general format the autograder is expecting
	return df.iloc[0]

# You can examine what your function returns by calling it in the cell. If you have questions
# about the assignment formats, check out the discussion forums for any FAQs
answer_zero()


# ### Question 1
# Which country has won the most gold medals in summer games?
#
# *This function should return a single string value.*

# In[ ]:

def answer_one():
	return df['Gold'].argmax()


# ### Question 2
# Which country had the biggest difference between their summer and winter gold medal counts?
#
# *This function should return a single string value.*

# In[ ]:

def answer_two():
	return (df['Gold']-df['Gold.1']).argmax()


# ### Question 3
# Which country has the biggest difference between their summer gold medal counts and winter gold medal counts relative to their total gold medal count?
#
# $$\frac{Summer~Gold - Winter~Gold}{Total~Gold}$$
#
# Only include countries that have won at least 1 gold in both summer and winter.
#
# *This function should return a single string value.*

# In[ ]:

def answer_three():
    copy_df = df.copy()
    copy_df = copy_df[(copy_df['Gold']>0) & (copy_df['Gold.1']>0)]
    return ((copy_df['Gold']-copy_df['Gold.1'])/copy_df['Gold.2']).argmax()


# ### Question 4
# Write a function that creates a Series called "Points" which is a weighted value where each gold medal (`Gold.2`) counts for 3 points, silver medals (`Silver.2`) for 2 points, and bronze medals (`Bronze.2`) for 1 point. The function should return only the column (a Series object) which you created.
#
# *This function should return a Series named `Points` of length 146*

# In[ ]:

def answer_four():
    df['Points'] = df['Gold.2']*3 + df['Silver.2']*2 + df['Bronze.2']
    return df['Points']


# ## Part 2
# For the next set of questions, we will be using census data from the [United States Census Bureau](http://www.census.gov/popest/data/counties/totals/2015/CO-EST2015-alldata.html). Counties are political and geographic subdivisions of states in the United States. This dataset contains population data for counties and states in the US from 2010 to 2015. [See this document](http://www.census.gov/popest/data/counties/totals/2015/files/CO-EST2015-alldata.pdf) for a description of the variable names.
#
# The census dataset (census.csv) should be loaded as census_df. Answer questions using this as appropriate.
#
# ### Question 5
# Which state has the most counties in it? (hint: consider the sumlevel key carefully! You'll need this for future questions too...)
#
# *This function should return a single string value.*

# In[ ]:

census_df = pd.read_csv('..\cfg\co-est2015-alldata.csv', encoding='gbk')
census_df.head()


# In[ ]:

def answer_five():
    return census_df['STNAME'].value_counts().argmax()


def answer_five_me():
    states = census_df['STNAME'].unique()
    census_df = census_df.set_index(['STNAME', 'CTYNAME'])
    census_df = census_df.sort_index(level='STNAME')

    result = pd.DataFrame(columns=['stataname', 'countryNum'])
    for state in states:
        state_countries = census_df.loc[(state, slice(None)), :]
        state_countries
        coutryNum = state_countries.count()[0]
        result = result.append(pd.Series(data={'stataname': state, 'countryNum': coutryNum}), ignore_index=True)

    sort_result = result.sort_values(by=['countryNum'], ascending=False)

    print("美国县最多的州的名字:\n", sort_result.iloc[0]['stataname'], sort_result.iloc[0]['countryNum'])


# ### Question 6
# Only looking at the three most populous counties for each state, what are the three most populous states (in order of highest population to lowest population)? Use `CENSUS2010POP`.
#
# *This function should return a list of string values.*
#
# In[ ]:

def answer_six():
    copy_df = census_df.copy()
    copy_df = copy_df.groupby(['STNAME'])
    states_pop = pd.DataFrame(columns=['pop'])
    for i, c in copy_df:
        # c.sort_values(by='CENSUS2010POP', ascending=False) ==> 先对当前州的所有县以人口排序
        # [1:4] ==> 然后取人口最多的前三个, 从第2到4行，因为groupby后，第一行是州的总量，具体的县是从第二行开始的
        # ['CENSUS2010POP'].sum() ==> 然后对CENSUS2010POP，取这三个县的总和，最后把三县人口总和作为结果保存到states_pops
        states_pop.loc[i] = [c.sort_values(by='CENSUS2010POP', ascending=False)[1:4]['CENSUS2010POP'].sum()]

    #最后states_pop得到的是各个州人口最多的三县人口总和，取最大的前三个nlargest(3,'pop')
    top3 = states_pop.nlargest(3,'pop')

    return list(top3.index)

def answer_six_me():
    census_df = pd.read_csv('..\cfg\co-est2015-alldata.csv', encoding='gbk')
    states = census_df['STNAME'].unique()
    census_df = census_df.set_index(['STNAME', 'CTYNAME'])
    census_df = census_df.sort_index(level='STNAME')
    result = pd.DataFrame(columns=['stateName', 'countryName', 'pop'])

    for state in states:
        # 得到每个州的所有县的DataFrame
        # if(state == 'Alabama'):

        state_countries = census_df.loc[(state, slice(None)), :]
        # 对人口进行降序排序
        state_countries = state_countries.sort_values(by=['CENSUS2010POP'], ascending=False)

        # 取排序后的前三个，也就是人口最多的三个country
        # 如果一个州的县小于3，则按照实际取值
        resultNum = 3 if len(state_countries) > 2 else len(state_countries)
        # print(resultNum)
        for i in range(resultNum):
            # 二重索引的元组，(index1, index2),i表示第i行的索引
            # print(state_countries.index[i])

            # [i][0]为二重索引的外层所以，[i][1]为二重索引的内层索引，
            countryName = state_countries.index[i][1]
            popNum = state_countries.iloc[i]['CENSUS2010POP']
            # print(state_countries.index[i][0],countryName,popNum)
            result = result.append(pd.Series(data={'stateName': state,
                                                   'countryName': countryName,
                                                   'pop': popNum}),
                                   ignore_index=True)


# ### Question 7
# Which county has had the largest absolute change in population within the period 2010-2015? (Hint: population values are stored in columns POPESTIMATE2010 through POPESTIMATE2015, you need to consider all six columns.)
#
# e.g. If County Population in the 5 year period is 100, 120, 80, 105, 100, 130, then its largest change in the period would be |130-80| = 50.
#
# *This function should return a single string value.*

# In[ ]:

def answer_seven():
    census_df = pd.read_csv('census.csv')
    pop = census_df[['STNAME','CTYNAME','POPESTIMATE2015','POPESTIMATE2014','POPESTIMATE2013','POPESTIMATE2012','POPESTIMATE2011','POPESTIMATE2010']]
    #pop['STNAME']!=pop['CTYNAME'] 去掉所有州总和的那一行
    pop = pop[pop['STNAME']!=pop['CTYNAME']]
    #每行的最大值 max(axis=1) 减去每行最小值 min(axis=1)，后取最大值的索引 argmax()
    index = (pop.max(axis=1)-pop.min(axis=1)).argmax()
    #用得到的index，去原表中取对应那一行，再取这一行的CTYNAME的值
    return census_df.loc[index]['CTYNAME']

def answer_seven_me():
    pop2010_2015 = census_df[
        ['POPESTIMATE2010', 'POPESTIMATE2011', 'POPESTIMATE2012', 'POPESTIMATE2013', 'POPESTIMATE2014',
         'POPESTIMATE2015']]
    # print("pop 2010-2015: \n",pop2010_2015.head(5))

    pop2010_2015['Max-Min'] = pop2010_2015.max(axis=1) - pop2010_2015.min(axis=1)
    pop2010_2015 = pop2010_2015.sort_values(by=['Max-Min'], ascending=False)
    print("pop 2010-2015: \n", pop2010_2015.index[0][1])


# ### Question 8
# In this datafile, the United States is broken up into four regions using the "REGION" column.
#
# Create a query that finds the counties that belong to regions 1 or 2, whose name starts with 'Washington', and whose POPESTIMATE2015 was greater than their POPESTIMATE 2014.
#
# *This function should return a 5x2 DataFrame with the columns = ['STNAME', 'CTYNAME'] and the same index ID as the census_df (sorted ascending by index).*

# In[ ]:
def answer_eight():
    # (census_df['REGION']<3 ) ==> REGION 为1/2的行
    # (census_df['CTYNAME'] == 'Washington County') ==> whose name starts with 'Washington'
    # (census_df['POPESTIMATE2015']>census_df['POPESTIMATE2014']) ==> POPESTIMATE2015 was greater than their POPESTIMATE 2014
    # [['STNAME','CTYNAME']]最后对结果取两列
    return census_df[(census_df['REGION'] < 3) & (census_df['CTYNAME'] == 'Washington County') & (
    census_df['POPESTIMATE2015'] > census_df['POPESTIMATE2014'])][['STNAME', 'CTYNAME']]


def answer_eight_me():
    census_df = pd.read_csv('..\cfg\co-est2015-alldata.csv', encoding='gbk')
    regions = census_df['REGION'].unique()
    print(regions)
    census_df = census_df.set_index(['REGION', 'CTYNAME'])
    census_df = census_df[['STNAME', 'POPESTIMATE2014', 'POPESTIMATE2015']]
    # result = pd.DataFrame(columns=['stateName','countryName','pop'])
    # print(census_df.head(3))
    for region in regions:
        if region == 1 or region == 2:
            census_df_region3 = census_df.loc[(region, slice(None)), :]
            census_df_region3 = census_df_region3.where(
                census_df_region3['POPESTIMATE2015'] > census_df_region3['POPESTIMATE2014']).dropna()
            census_df_region3 = census_df_region3.reset_index()
            census_df_region3 = census_df_region3.where(
                (census_df_region3['CTYNAME']).str.contains('Washington')).dropna()
            result = census_df[(census_df[['REGION']] == census_df_region3[['REGION']]) & (
            census_df[['CTYNAME']] == census_df_region3[['CTYNAME']]) & (
                               census_df['STNAME'] == census_df_region3['STNAME'])]
            print(result)