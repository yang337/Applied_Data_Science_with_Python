
# coding: utf-8

# ---
# 
# _You are currently looking at **version 1.1** of this notebook. To download notebooks and datafiles, as well as get help on Jupyter notebooks in the Coursera platform, visit the [Jupyter Notebook FAQ](https://www.coursera.org/learn/python-data-analysis/resources/0dhYG) course resource._
# 
# ---

# In[1]:

import pandas as pd
import numpy as np
from scipy.stats import ttest_ind


# # Assignment 4 - Hypothesis Testing
# This assignment requires more individual learning than previous assignments - you are encouraged to check out the [pandas documentation](http://pandas.pydata.org/pandas-docs/stable/) to find functions or methods you might not have used yet, or ask questions on [Stack Overflow](http://stackoverflow.com/) and tag them as pandas and python related. And of course, the discussion forums are open for interaction with your peers and the course staff.
# 
# Definitions:
# * A _quarter_ is a specific three month period, Q1 is January through March, Q2 is April through June, Q3 is July through September, Q4 is October through December.
# * A _recession_ is defined as starting with two consecutive quarters of GDP decline, and ending with two consecutive quarters of GDP growth.
# * A _recession bottom_ is the quarter within a recession which had the lowest GDP.
# * A _university town_ is a city which has a high percentage of university students compared to the total population of the city.
# 
# **Hypothesis**: University towns have their mean housing prices less effected by recessions. Run a t-test to compare the ratio of the mean price of houses in university towns the quarter before the recession starts compared to the recession bottom. (`price_ratio=quarter_before_recession/recession_bottom`)
# 
# The following data files are available for this assignment:
# * From the [Zillow research data site](http://www.zillow.com/research/data/) there is housing data for the United States. In particular the datafile for [all homes at a city level](http://files.zillowstatic.com/research/public/City/City_Zhvi_AllHomes.csv), ```City_Zhvi_AllHomes.csv```, has median home sale prices at a fine grained level.
# * From the Wikipedia page on college towns is a list of [university towns in the United States](https://en.wikipedia.org/wiki/List_of_college_towns#College_towns_in_the_United_States) which has been copy and pasted into the file ```university_towns.txt```.
# * From Bureau of Economic Analysis, US Department of Commerce, the [GDP over time](http://www.bea.gov/national/index.htm#gdp) of the United States in current dollars (use the chained value in 2009 dollars), in quarterly intervals, in the file ```gdplev.xls```. For this assignment, only look at GDP data from the first quarter of 2000 onward.
# 
# Each function in this assignment below is worth 10%, with the exception of ```run_ttest()```, which is worth 50%.

# In[95]:

# Use this dictionary to map state names to two letter acronyms
states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
import numpy as np
import pandas as pd
from scipy.stats import ttest_ind


# In[3]:

def get_list_of_university_towns():
    '''Returns a DataFrame of towns and the states they are in from the 
    university_towns.txt list. The format of the DataFrame should be:
    DataFrame( [ ["Michigan", "Ann Arbor"], ["Michigan", "Yipsilanti"] ], 
    columns=["State", "RegionName"]  )
    
    The following cleaning needs to be done:

    1. For "State", removing characters from "[" to the end.
    2. For "RegionName", when applicable, removing every character from " (" to the end.
    3. Depending on how you read the data, you may need to remove newline character '\n'. '''
    
    df = pd.read_csv('university_towns.txt', sep = ';', names=['RegionName'])
    df.insert(loc = 0, column = 'State', value = df['RegionName'].str.extract(r'(.*)\[edit\]').ffill())
    df['RegionName'] = df['RegionName'].str.replace(r' \(.*$', '')
    df = df[~df['RegionName'].str.contains(r'\[edit\]')].reset_index(drop = True)
    
    #replace state names with two letter acronyms
#     states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National', 'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana', 'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho', 'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan', 'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico', 'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa', 'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana', 'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California', 'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island', 'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia', 'ND': 'North Dakota', 'VA': 'Virginia'}
#     states2 = {v: k for k, v in states.items()}
#     df.replace({"State": states2}, inplace = True)

    return df


# In[4]:

def get_recession_start():
    '''Returns the year and quarter of the recession start time as a 
    string value in a format such as 2005q3'''
    
    df = pd.read_excel('gdplev.xls', skiprows = 220, usecols = [4,6], header = None)
    df.columns = ['quarter', 'GDP']
    for i in range(2, len(df)):
        if (df.iloc[i-1][1] < df.iloc[i-2][1]) and (df.iloc[i][1] < df.iloc[i-1][1]):
            return df.iloc[i-1][0]


# In[5]:

def get_recession_end():
    '''Returns the year and quarter of the recession end time as a 
    string value in a format such as 2005q3'''
       
    df = pd.read_excel('gdplev.xls', skiprows = 220, usecols = [4,6], header = None)
    df.columns = ['quarter', 'GDP']
    start = get_recession_start()
    start_ind = df[df['quarter'] == start].index.tolist()[0]
    for i in range(start_ind, len(df)):
        if (df.iloc[i-1][1] > df.iloc[i-2][1]) and (df.iloc[i][1] > df.iloc[i-1][1]):
            return df.iloc[i][0]


# In[6]:

def get_recession_bottom():
    '''Returns the year and quarter of the recession bottom time as a 
    string value in a format such as 2005q3'''
    
    df = pd.read_excel('gdplev.xls', skiprows = 220, usecols = [4,6], header = None)
    df.columns = ['quarter', 'GDP']
    start = get_recession_start()
    start_ind = df[df['quarter']==start].index.tolist()[0]
    end = get_recession_end()
    end_ind = df[df['quarter']==end].index.tolist()[0]
    recession = df.iloc[start_ind:end_ind + 1]
    bot = recession['GDP'].argmin()
    
    return df['quarter'].iloc[bot]


# In[52]:

def convert_housing_data_to_quarters():
    '''Converts the housing data to quarters and returns it as mean 
    values in a dataframe. This dataframe should be a dataframe with
    columns for 2000q1 through 2016q3, and should have a multi-index
    in the shape of ["State","RegionName"].
    
    Note: Quarters are defined in the assignment description, they are
    not arbitrary three month periods.
    
    The resulting dataframe should have 67 columns, and 10,730 rows.
    '''
    
    df = pd.read_csv('City_Zhvi_AllHomes.csv')
    df['State'] = df['State'].map(states)
    df.set_index(['State', 'RegionName'], inplace = True)
    cols = df.columns.tolist()[49:]
    df = df[cols]
    #method 1:
    seg_month = [df.columns.tolist()[x:x+3] for x in range(0, len(df.columns), 3)]
    year = list(range(2000, 2017))
    quar = ['q1', 'q2', 'q3', 'q4']
    quarters = [str(y) + q for y in year for q in quar]
    quarters = quarters[:-1]
    for q, ms in zip(quarters, seg_month):
    #     print(q), print(ms), print('\n')
        df[q] = df[ms].mean(axis = 1)
    df = df[quarters]
    
    return df
# list(range(0,10,2))
# housing = housing.resample('Q',axis=1).mean()

##Another method:
# df.columns = pd.to_datetime(df.columns)
# df.resample('Q', axis = 1).mean().rename(columns=lambda x: str(x.to_period('Q')).lower())


# In[106]:

def run_ttest():
    '''First creates new data showing the decline or growth of housing prices
    between the recession start and the recession bottom. Then runs a ttest
    comparing the university town values to the non-university towns values, 
    return whether the alternative hypothesis (that the two groups are the same)
    is true or not as well as the p-value of the confidence. 
    
    Return the tuple (different, p, better) where different=True if the t-test is
    True at a p<0.01 (we reject the null hypothesis), or different=False if 
    otherwise (we cannot reject the null hypothesis). The variable p should
    be equal to the exact p value returned from scipy.stats.ttest_ind(). The
    value for better should be either "university town" or "non-university town"
    depending on which has a lower mean price ratio (which is equivilent to a
    reduced market loss).'''
    
    start = get_recession_start() #2008q3
    btm = get_recession_bottom()  #2009q2
    housing = convert_housing_data_to_quarters()
    univ = get_list_of_university_towns()
    housing['ratio'] = housing.iloc[:, housing.columns.get_loc(start)-1] / housing[btm]
    housing = housing['ratio'].reset_index()

    df = pd.merge(housing.reset_index(), univ, how = 'outer', on = univ.columns.tolist(), indicator = '_flag')
    group_univ = df[df['_flag']=='both'].loc[:, 'ratio'].dropna()
    group_other = df[df['_flag']!='both'].loc[:, 'ratio'].dropna()

    pvalue = list(ttest_ind(group_univ, group_other))[1]
    different = pvalue < 0.01
    if group_univ.mean() < group_other.mean():
        better = 'university town'
    else:
        better = 'non-university town'

    return (different, pvalue, better)



# https://www.coursera.org/learn/python-data-analysis/discussions/weeks/4/threads/F6mWJ7SbEeeKBBKJgknU5g
# PriceRatio=QuarterBeforeRecessionStart / RecessionBottomQuarte


# In[ ]:




# In[ ]:



