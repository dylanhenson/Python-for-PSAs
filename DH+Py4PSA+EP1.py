
# coding: utf-8

# In[68]:


import requests
from bs4 import BeautifulSoup, Comment
import pandas as pd
#BeautifulSoup


# In[52]:


BASE_URL = 'https://www.baseball-reference.com/teams/CHC/2017.shtml'

response = requests.get(BASE_URL)


# In[53]:


#response.text


# In[54]:


soup = BeautifulSoup(response.text, 'lxml')
#soup


# In[55]:


#dir(soup)


# In[58]:


table = soup.find_all(id='appearances')

comments=soup.find_all(string=lambda text:isinstance(text,Comment))
#comments is a list, the elements in the list are the comments from the URL

for element in comments:
    if 'id="appearances"' in element:
        player_info = element


# In[77]:


soup = BeautifulSoup(player_info, 'lxml')

body = soup.find('tbody')
headers = soup.find_all('thead')

column_headers = []
for element in headers:
    element.find_all('th')
#        column_headers_headers.append(element.text)

print(column_headers)    
    
all_player_data = []
for row in body.find_all('tr'):
    player_name = row.find('th')
    player_data = [player_name.text]
    for data in row.find_all('td'):
        player_data.append(data.text)
    all_player_data.append(player_data)


# In[72]:


all_player_data

df = pd.DataFrame(all_player_data)
#my_list = [['data','data_1'],['hello',''],]


# In[70]:


df.head()

