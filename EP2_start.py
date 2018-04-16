
# coding: utf-8

# In[6]:


# import all of the tools (packages) we will be needing to complete todays excersize

#requests is a package for getting raw html from websites. You can do things like login, store info, etc
#for today we will just be using it to simply get content.
import requests

#BeautifulSoup is THE package for parseing HTML. The Comment class we import is used for extracting <---COMMENTED OUT---> content.
from bs4 import BeautifulSoup, Comment

#pandas is one of the most widely used data management packages in python. It is great for working with any kind of tabular data.
import pandas as pd


# In[15]:



#we create these variables as we want to be able to track which team we are looking at, and also which season.
year = 2017
team = 'CHC'

def get_table(team, year):
    
    #get all the raw html from the page, and store it in the variable 'response'
    #we use an f'' string here, this is a string where anything in {} curly braces gets evaluated to a string.
    #eg {year} evaluates to the string '2017'
    BASE_URL = f'https://www.baseball-reference.com/teams/{team}/{year}.shtml'
    response = requests.get(BASE_URL)
    #create our first batch of soup! BeautifulSoup returns content which has a bunch of method for PARSING (extracting meaninful content from) raw data
    soup = BeautifulSoup(response.text, 'lxml')
        #by using crtl+shift+i in Chrome we open up developer tools, we can then see that the table we are looking for has the attribute id='appearances'
    table = soup.find_all(id='appearances')
    #but wait - why is print(table) empty? If we look at the page source, we can see that the table is <--COMMENTED OUT-->,
    #this means we can't just get it via our 'normal' soup.find/soup.find_all methods. 
    #fortunately - we can look for commented out content specifically, yay progress! This is why we imported Comment up the top


    #soup.find_all accepts lambda functions as valid arguements, though it is a little confusing to read,
    #the content between the brackets is roughly equivalent to the pseudocode:
    #go through the entire document, element by element.
    #if the text of that element is a Comment (aka if it is an instance of Comment class)
    #then add that element to the variable 'comments'
    comments=soup.find_all(string=lambda text:isinstance(text,Comment))

    #now lets look at each of those elements one at a time
    for element in comments:
        #to select the correct element from our list, we need something to identify it - fortunately, we know the id is unique, so can use that.
        if 'id="appearances"' in element:
            #once we have identified the correct element, we assign it to player_info so we can access it later.
            player_info = element


    #BONUS - why this is commented out(advanced).
    #requests module looks at server responses. However, the server responds with this content commented out.
    #The client side .JS then uncomments the content once the page is loaded. This can be done for many reasons - mostly performance,
    #but also for sites trying to prevent data scraping.
    #this is also why we can not get the table contents directly with pd.read_html(f'https://www.baseball-reference.com/teams/{team}/{year}.shtml')
        #the previus cell leaves us with'player_info' as a string, this is the correct data we want, but we need to convert it to BeautifulSoup
    #to open up the html filtering functionality. We use 'lxml' formatting again, as we will with 99% of websites as this covers modern HTML5 well.
    soup = BeautifulSoup(player_info, 'lxml')

    #the main methods we will be using are soup.find and soup.find_all. soup.find() returns a single value (the first that meets the condition)
    #, where soup.find_all() returns a list [] of ALL elements which meet the criteria inside the brackets.

    #we extract the body and the header of the table as seperate items. 
    body = soup.find('tbody')

    #UPDATE - in tutorial we had this using find_all, which is incorrect, as there is only 1 header for this table.
    headers = soup.find('thead')

    #inside the header we have many 'th' elements - which are 'column headers', we extract all of these and store them in a list:
    column_headers = []
    for value in headers.find_all('th'):
            column_headers.append(value.text)

    #if you are starting a loop with empty brackets and filling them, it's a good sign you could use list comprehension (one liners)
    #the equivalent one-liner is:
    # column_headers = [value.text for value in headers.find_all('th)]


    #but for clarity lets do it in expanded form first
    all_player_data = []

    #get all rows in the body
    for row in body.find_all('tr'):

        #the player name is the only element in the row that is a 'th'
        player_name = row.find('th')

        #we need to also track the year and the team
        player_data = [year, team, player_name.text] 

        #all the rest of the row in 'td' so we use find_all to extract them, then add the text to the list we are storing that rows content in
        for data in row.find_all('td'):
            player_data.append(data.text)
        all_player_data.append(player_data)

    #printing the first 2 elements of all_player_data just so we can see what it is
    print(all_player_data[:2])
    
    #GREAT now we have the table header, and all the data sucessfully extracted. However, there is some data we do not have which we want.
    #namely, we need to track the TEAM and the YEAR for the data. also note that some elements in the header list are blank.
    #to complete our data set we need to add these in. You _could_ scrape this, but it's only 3 elements so manual is fine

    missing_values = ['Year','Team']
    column_headers = missing_values + column_headers
    #we have now added these two values to the start of the headers
    #now lets address the blank values, remember python is 0-indexed, so the first element in a list can be referenced by [0] - this is called a slice
    column_headers[4] = 'Country'

    #we also want to add to the end, you can do this using a negative slice
    column_headers[-1] = 'All Star'

    #note - Jupyter notebooks automatically print variables if they are called. Normally you would need to explicitly call
    #print(column_headers) 
    column_headers
    #now we create our dataframe! For information on this see here: https://pandas.pydata.org/pandas-docs/stable/generated/pandas.DataFrame.html
    
    return all_player_data, column_headers

all_teams = ['ARI', 'ATL', 'BAL', 'BOS', 'CHC', 'CHW', 'CIN', 'CLE', 'COL', 'DET', 'HOU', 'KCR', 'ANA', 'LAD', 'FLA', 'MIL', 'MIN', 'NYM', 'NYY', 'OAK', 'PHI', 'PIT', 'SDP', 'SFG', 'SEA', 'STL', 'TBD', 'TEX', 'TOR', 'WSN']
all_data = []
for year in range(2016,2017):
    for team in all_teams:
        print(f'currently processing {team} for {year}')
        
        try:
            all_player_data, column_headers = get_table(team,year)
            
            all_data = all_data + all_player_data #Could also use all_data += all_player_data
        except Exception as e:
                print(e)
                continue
        

#print(get_table('CHC','2017'))


# In[19]:


#Write to excel

df = pd.DataFrame(all_data, columns = column_headers)##### FILL THIS OUT
writer = pd.ExcelWriter('baseball_output.xlsx')
df.to_excel(writer, 'baseball_stats')
writer.save()


# In[13]:


#Example showing return vs print

def say_hello(name):
    print('hello' + ' ' + name)

say_hello('Dilly')
#Not working


# In[ ]:



df = pd.DataFrame(all_player_data, columns=column_headers)

#df.head prints the top 5 rows of a dataframe. The ... in the middle means there is columns which aren't printing, because the table is too wide.
#this isn't an issue as we know the data is there.
df.head(100)


# In[ ]:


#Awesome! We have our one table of data, correctly formatted and ready for analysis. But this is only one year!
#in the next session we will expand this to be able to get data across a range of time and teams.


# In[4]:


#Creating a function
def say_hello(name):
    print(f'hello {name}')


# In[5]:


say_hello('Dilly Dilly')

