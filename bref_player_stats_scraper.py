
# coding: utf-8

# In[61]:


from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
import time


# In[62]:


# Create url templates for each kind of stats
per_g_url_template = "https://www.basketball-reference.com/leagues/NBA_{year}_per_game.html"
adv_url_template = "https://www.basketball-reference.com/leagues/NBA_{year}_advanced.html"
tot_url_template = "https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
per_36m_url_template = "https://www.basketball-reference.com/leagues/NBA_{year}_per_minute.html"
per_100p_url_template = "https://www.basketball-reference.com/leagues/NBA_{year}_per_poss.html"

# Put all the URL templates into a list
url_template_list = [per_g_url_template, adv_url_template, tot_url_template, 
                     per_36m_url_template,]


# In[63]:


# Create empty lists to store data before appending to Dataframe
column_headers = []
player_data = []
# Create empty DataFrame for following functions to fill
df = pd.DataFrame()


# In[64]:


# Empty DataFrames for each set of pages
df_adv = pd.DataFrame()
df_per_g = pd.DataFrame()
df_tot = pd.DataFrame()
df_per_36m = pd.DataFrame()
#df_per_100p = pd.DataFrame

# Create df_list of DataFrames for looping
df_list = [df_per_g, df_adv, df_tot, df_per_36m]


# In[65]:


# Get column headers from each page
# Assigns a new list of column headers each time this is called
def get_column_headers(soup):
    headers = []
    for th in soup.find('tr').findAll('th'):
        #print th.getText()
        headers.append(th.getText())
    #print headers # this line was for a bug check
    # Assign global variable to headers gathered by function
    return headers    
    #column_headers = [th.getText() for th in soup.find('tr').findAll('th')]


# In[66]:


# old function that's a mess
def get_player_data(soup):
    temp_player_data = []
    for i in range(len(soup.findAll('tr')[1:])):
        # temp list to store player data
        player_row = []
        
        # Loop through 'td' tags to extract player data
        for td in soup.findAll('tr')[1:][i].findAll('td'):
            player_row.append(td.getText())
        
        # Append data to a list    
        temp_player_data.append(player_row)
        
        # Replace global variable with gathered player data
    print(temp_player_data)
    player_data = temp_player_data


# In[67]:


# Function to get player data from each page
def get_player_data(soup):
    # Temporary list within function to store data
    temp_player_data = []
    
    data_rows = soup.findAll('tr')[1:] # skip first row
    for i in range(len(data_rows)): # loop through each table row
        player_row = [] # empty list for each player row
        for td in data_rows[i].findAll('td'):
            player_row.append(td.getText()) # append separate data points
        temp_player_data.append(player_row) # append player row data
    return temp_player_data


# In[68]:


def scrape_page(url):
    r = requests.get(url) # get the url
    soup = BeautifulSoup(r.text, 'html.parser') # Create BS object
    
    # call function to get column headers
    column_headers = get_column_headers(soup)
    
    # call function to get player data
    player_data = get_player_data(soup)
    
    # input data to DataFrame
    # Skip first value of column headers, 'Rk'
    df = pd.DataFrame(player_data, columns = column_headers[1:])
    
    return df


# In[69]:


def get_season(input_year):
    first_yr = input_year - 1
    season = str(first_yr) + "-" + str(input_year)[2:]
    return season


# In[70]:


# This function drops empty rows an columns, drops duplicates, and changes
# % character in columns
def gen_cleaning(df):
    # Convert values to numeric values first
    df = df.apply(pd.to_numeric, errors = 'ignore')
    
    # Drop columns with no data
    df.dropna(axis = 1, how = "all", inplace = True)
    
    # Drop rows with no data
    df.dropna(axis = 0, how = "all", inplace = True)
    
    # Remove duplicates player inputs; ie. players who were traded
    # I only kept the TOT per game season values
    #df.drop_duplicates(["Player"], keep = "first", inplace = True)
    
    # Change % symbol to _perc
    df.columns = df.columns.str.replace('%', '_perc')
    
    return df


# In[71]:


# This function scrapes player data from multiple pages by start and end years
def scrape_pages(url_template, start_year, end_year, output_df):
    count = 0 
    for year in range(start_year, (end_year+1)):
        url = url_template.format(year = year) # grab URL per year
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'html5lib') # Create soup item
        
        # Check to grab column headers
        if count == 0: # only append column headers once
            columns = get_column_headers(soup)
            count += 1
            
        # grab player data for each year
        player_data = get_player_data(soup)
        
        # Create temporary DataFrame first for each year
        # Duplicates are removed before putting into bigger DataFrame
        # These duplicates come from players playing on multiple teams in one season
        # This script only keeps the TOT output as Tm
        year_df = pd.DataFrame(player_data, columns = columns[1:])
        year_df.drop_duplicates(['Player'], keep = 'first', inplace = True)
        year_df.insert(0, 'Season', get_season(year)) # insert season year column
        
        # Append to big DataFrame for detailed cleaning
        output_df = output_df.append(year_df, ignore_index = True)
        
    # Do common, general cleaning practices
    output_df = gen_cleaning(output_df)
        
    return output_df


# In[72]:


# This bunch of code is just for me to check things as I go

#url = "https://www.basketball-reference.com/leagues/NBA_2006_per_game.html"
#r = requests.get(url)
#soup = BeautifulSoup(r.text, 'html.parser')
#column_headers = get_column_headers(soup)
#player_data = get_player_data(soup)
#df_test = pd.DataFrame(player_data, columns = column_headers[1:])
#df_test = gen_cleaning(df_test)


# In[73]:


#df_test.sort_values('PS/G', ascending = False)


# In[74]:


#df_test[df_test['Player'] == 'Kobe Bryant']


# In[75]:


# Fill each DataFrame with data scraped from their respective pages
# Each print statement is a check for if any pages or functions give issues
# Added timer to check how long this was taking

start = time.time()

df_per_g = scrape_pages(per_g_url_template, 1981, 2017, df_per_g)
print("Finished per g")
df_adv = scrape_pages(adv_url_template, 1981, 2017, df_adv)
print("Finished adv")
df_tot = scrape_pages(tot_url_template, 1981, 2017, df_tot)
print("Finished tots")
df_per_36m = scrape_pages(per_36m_url_template, 1981, 2017, df_per_36m)
print("Finished per 36m")

end = time.time()
print("Time elapsed :" +str((end - start) / 60) + " minutes")


# In[76]:


# Check all column names to see what needs to be cleaned

print("totals")
print(list(df_tot))
print("per game")
print(list(df_per_g))
print("per 36 minutes")
print(list(df_per_36m))
print("advanced")
print(list(df_adv))


# In[77]:


# Label columns properly by adding "_tot" to the end of some column values
df_tot.columns.values[[7, 8 , 9, 11, 12, 14, 15, 18, 19]] = [df_tot.columns.values[[7, 8 , 9, 11, 12, 14, 15, 18, 19]][col] + "_tot" for col in range(9)]

df_tot.columns.values[21:30] = [df_tot.columns.values[21:30][col] + "_tot" for col in range(9)]


# In[78]:


# Check column titles again
list(df_tot)


# In[79]:


# drop _perc columns from per_g and per_36m
# Never mind, drop duplicates later on
# Add _per_g and _per_36m to column values
# Add _per_G to some values in df_per_g
df_per_g.columns.values[[7, 8 , 9, 11, 12, 14, 15, 18, 19]] = [df_per_g.columns.values[[7, 8 , 9, 11, 12, 14, 15, 18, 19]][col] + "_per_G" for col in range(9)]

df_per_g.columns.values[21:29] = [df_per_g.columns.values[21:30][col] + "_per_G" for col in range(8)]

# Rename PS/G to PTS_per_G
df_per_g.rename(columns={'PS/G': 'PTS_per_G'}, inplace = True)


# In[80]:


df_per_36m.columns.values[[7, 8, 9, 11, 12, 14, 15, 18, 19]]


# In[81]:


# Check if proper values were changed
list(df_per_g)


# In[82]:


df_per_36m.columns.values[[8, 9, 11, 12, 14, 15, 17, 18]] = [df_per_36m.columns.values[[8, 9, 11, 12, 14, 15, 17, 18]][col] + "_per_36m" for col in range(8)]

df_per_36m.columns.values[20:30] = [df_per_36m.columns.values[20:30][col] + "_per_36m"                                    for col in range(9)]


# In[83]:


# Check columns were changed properly
list(df_per_36m)


# In[84]:


# Find where '\xa0' columns are for removal
print(df_adv.columns[-5])
print(df_adv.columns[19])


# In[25]:


# Drop '\xa0' columns, last one first
#df_adv.drop(df_adv.columns[-5], axis = 1, inplace = True)
#df_adv.drop(df_adv.columns[19], axis = 1, inplace = True)


# In[85]:


list(df_adv)


# In[86]:


df_adv.rename(columns = {'WS/48' : 'WS_per_48'}, inplace = True)


# In[87]:


# Check to see if columns were dropped properly
list(df_adv)


# In[28]:


# Merge dataframes later on season, player name, and team
# Order of merges: tots, per_g, per_36m, adv
# DFs: df_tot, df_per_g, df_per_36m, df_adv
# Common things: Season, Player, Pos, Age, Tm, G


# In[88]:


df_all = pd.merge(df_tot, df_per_g, how = "left", 
                 on = ['Season', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'FT_perc',
                      '3P_perc', '2P_perc', 'FG_perc', 'eFG_perc'])


# In[89]:


df_all = pd.merge(df_all, df_per_36m, how = "left",
                 on = ['Season', 'Player', 'Pos', 'Age', 'Tm', 'G', 'GS', 'FT_perc',
                      '3P_perc', '2P_perc', 'FG_perc'])


# In[90]:


df_all = pd.merge(df_all, df_adv, how = "left",
                on = ['Season', 'Player', 'Pos', 'Age', 'Tm', 'G'])


# In[91]:


# Check columns to make sure they're all right
list(df_all)


# In[33]:


# Try to drop duplicate MP columns
list(df_all.drop(['MP_x', 'MP_y'], axis = 1))


# In[92]:


df_all.drop(['MP_x', 'MP_y'], axis = 1, inplace = True)


# In[93]:


# Final check of columns
list(df_all)


# In[103]:


# Create a DataFrame with top 25 single season scorers 
df_top_25_scorers = df_all.sort_values('PTS_per_G', ascending = False).head(n=25)


# In[106]:


df_top_50_scorers = df_all.sort_values('PTS_per_G', ascending = False).head(n=50)


# In[95]:


len(df_top_scorers)


# In[104]:


df_top_25_scorers[['Season', 'Player', 'PTS_per_G']]


# In[97]:


df_all[df_all['Player'] == 'Kevin Durant'][['Season', 'Player', 'PTS_per_G']]


# In[112]:


# I think this position is a mistake
df_all[df_all['Pos'] == 'C-SF']


# In[111]:


df_all[df_all['Pos'] == 'PG-SF']


# In[98]:


# Write to CSV files and DONE!
df_all.to_csv("bref_1981_2017_player_data.csv", encoding = 'utf-8', index = False)


# In[105]:


df_top_25_scorers.to_csv("bref_1981_2017_top_25_season_scorers.csv", encoding = 'utf-8', index = False)


# In[107]:


df_top_50_scorers.to_csv("bref_1981_2017_top_50_season_scorers.csv", encoding = "utf-8", index = False)

