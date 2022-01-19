def us_tax_calculator_single(income, bracket = 'single'):
    if (bracket =='single') & (income >= 518400):
        return (income-518400)*0.37 + (9875*0.10) + (40125-9875)*0.12 + (85525-40125)*0.22 +(163300-85525)*0.24 + (207350 - 163300)*0.32 + (518400-207350)*0.35
    elif (bracket =='single') & (income >= 207350):
        return (income-207350)*0.35 + (9875*0.10) + (40125-9875)*0.12 + (85525-40125)*0.22 +(163300-85525)*0.24 + (207350 - 163300)*0.32
    elif (bracket =='single') & (income >= 163300):
        return (income-163300)*0.32 + (9875*0.10) + (40125-9875)*0.12 + (85525-40125)*0.22 +(163300-85525)*0.24
    elif (bracket =='single') & (income >= 85525):
        return (income-85525)*0.24 + (9875*0.10) + (40125-9875)*0.12 + (85525-40125)*0.22
    elif (bracket =='single') & (income >= 40125):
        return (income-40125)*0.22 + (9875*0.10) + (40125-9875)*0.12
    elif (bracket =='single') & (income >= 9875):
        return (income-9875)*0.12 + (9875*0.10)
    else:
        return income*0.10
def us_tax_calculator_double(income, bracket = 'double'):        
    if (bracket =='double') & (income >= 622050):
        return (income-622050)*0.37 + (9875*0.10) + (40125-9875)*0.12 + (171050-40125)*0.22 +(326600-171050)*0.24 + (414700 - 326600)*0.32 + (622050-414700)*0.35
    elif (bracket =='double') & (income >= 414700):
        return (income-414700)*0.35 + (9875*0.10) + (40125-9875)*0.12 + (171050-40125)*0.22 +(326600-171050)*0.24 + (414700 - 326600)*0.32
    elif (bracket =='double') & (income >= 326600):
        return (income-326600)*0.32 + (9875*0.10) + (40125-9875)*0.12 + (171050-40125)*0.22 +(326600-171050)*0.24
    elif (bracket =='double') & (income >= 171050):
        return (income-171050)*0.24 + (9875*0.10) + (40125-9875)*0.12 + (171050-40125)*0.22
    elif (bracket =='double') & (income >= 80250):
        return (income-80250)*0.22 + (19750*0.10) + (80250-19750)*0.12
    elif (bracket =='double') & (income >= 19750):
        return (income-19750)*0.12 + (19750*0.10)
    elif (bracket =='double') & (income < 19750):
        return income*0.10
from bs4 import BeautifulSoup
import requests
import sqldf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
wiki_url = 'https://en.wikipedia.org/wiki/Taxation_in_Switzerland'
s = requests.Session()
response = s.get(wiki_url, timeout = 10)
soup = BeautifulSoup(response.content, 'html.parser')
right_table=soup.find('table', {"class":'wikitable sortable collapsible'})
for row in right_table.findAll("tr"):
    cells = row.findAll('td')
len(cells)
rows = right_table.findAll("tr")
header = [th.text.rstrip() for th in rows[1].find_all('th')]
lst_data1 = []
for row in rows[0:]:
            data = [d.text.rstrip() for d in row.select('td')]
            lst_data1.append(data)
taxes = lst_data1[2:]
cantons_url = 'https://en.wikipedia.org/wiki/Cantons_of_Switzerland'
s = requests.Session()
response = s.get(cantons_url, timeout = 10)
soup = BeautifulSoup(response.content, 'html.parser')
soup.title.string
right_table=soup.find('table', {"class":'sortable wikitable'})

canton_rows = right_table.findAll("th")
newdata = []
for row in canton_rows[0:]:
            data =  row.select('span')
            data = str(data)
            newdata.append(data)
import re
# Define the list and the regex pattern to match
pattern = '^.*language*'
# Filter out all elements that match the above pattern
filtered = [str(x.split('text')) for x in newdata if re.match(pattern, x)]
midway = [re.search('>(.*)<', string).group(0) for string in filtered]
midway = [str(x.split(',')) for x in midway]
midway = [str(x.split('span')) for x in midway]
midway = [re.search('>(.*)<', string).group(0) for string in midway]
import re
new_string = [re.sub('[><"/\,=]', '', old_string) for old_string in midway]
#new_string[1][:new_string[1].index(" ")]
new_string[0]
midway = [re.search('normal;.*\'', string).group(0) for string in new_string]
midway = [re.search(';.*\'', string).group(0) for string in midway]
midway = [re.search(r';(.*?)\'', string).group(0) for string in midway]
cantons = [re.sub('[;\']', '', old_string) for old_string in midway]
cantons
len(cantons)
federal_taxes = taxes[26]
taxes.pop(26)
cantons.pop(26)
federal_taxes.pop(7)
federal_taxes = [re.sub('[,]', '', tax) for tax in federal_taxes]
df = pd.DataFrame(data=taxes)
df.drop(df.columns[7], axis=1, inplace=True)
df['Cantons'] = cantons
df.columns = ['20000','40000', '60000', '80000', '100000', '200000', '500000', '20000', '40000', '60000', '80000', '100000', '200000', '500000', 'Cantons']
def federal_calculator(row):
    row = [re.sub('[,]', '', tax) for tax in row]
    newrow = [float(row[i]) + float(federal_taxes[i]) for i in range(0,14)]
    newrow.append(row[14])
    return newrow
newerdata = []
for i in range(0,len(df)):
    myrow = df.iloc[i]
    newrow = federal_calculator(myrow)
    newerdata.append(newrow)
newerdata[0]
df = pd.DataFrame(data = newerdata, columns = ['20000','40000', '60000', '80000', '100000', '200000', '500000', '20000', '40000', '60000', '80000', '100000', '200000', '500000', 'Cantons'])
single_df = df.iloc[:,0:7]
double_df = df.iloc[:,7:]
double_df.head()
single_df['Cantons'] = double_df['Cantons']
single_df = pd.melt(single_df, id_vars=['Cantons'])
double_df = pd.melt(double_df, id_vars=['Cantons'])
single_df.columns = ['Canton','Income','Swiss taxes']
double_df.columns = ['Canton','Income','Swiss taxes']
single_df['Income'] = single_df['Income'].apply(pd.to_numeric, errors = 'coerce')
double_df['Income'] = double_df['Income'].apply(pd.to_numeric, errors = 'coerce')
single_df['US Taxes'] = single_df['Income'].apply(us_tax_calculator_single)
double_df['US Taxes'] = double_df['Income'].apply(us_tax_calculator_double)
single_df.to_csv('.//data/single_payer.csv')
double_df.to_csv('.//data/double_payer.csv')
