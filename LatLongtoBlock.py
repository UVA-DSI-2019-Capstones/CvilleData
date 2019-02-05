
# coding: utf-8

# # Convert Lat/Long to Block Number

# Import libraries

# In[11]:


import pandas as pd
import sys
import time
import urllib.request
import re


# Read in arbitrary dataframe for testing

# In[5]:


racks = pd.read_csv('data/bicycle_rack_points.csv')


# Function to scrape FCC website for block number by lat/long. Just insert a dataframe with lat and long labeled as Y and X columns, respectively. It'll output a pandas Series of block numbers (you'll need to manually tack it on to the dataframe).

# In[8]:


def lltoblock(df):
    
    # Create empty array for storing block number
    block_list = pd.Series([])
    
    # Create opener
    opener = urllib.request.FancyURLopener({})
    
    if 'X' in df.columns and 'Y' in df.columns:
        lat = df['Y']
        lng = df['X']
    elif 'Latitude' in df.columns and 'Longitude' in df.columns:
        lat = df['Latitude']
        lng = df['Longitude']
    elif 'Meter_Lat' in df.columns and 'Meter_Long' in df.columns:
        lat = df['Meter_Lat']
        lng = df['Meter_Long']
    else:
        lat = None
        lng = None

    
    # Iterate over all rows of dataframe
    for i in range(len(df)):
        
        # Create url from lat/long
        url = 'https://geo.fcc.gov/api/census/block/find?latitude='        + str(lat[i]) + '&longitude=' + str(lng[i]) + '&showall=false&format=json'
        
        # Store webpage contents
        f = opener.open(url)
        content = f.read()
        
        # Get block number out of content string
        block = re.search(r".*FIPS\":\" *(.*?) *\",\"bbox.*", str(content)).group(1)
        
        # Add current block number to our block array
        block_list[i] = block
        
    # Return the list of block numbers
    return block_list


# Call the function on a test dataframe

# In[9]:


lltoblock(racks).head()


# In[10]:


lltoblock(pd.read_csv('./data/parking_meter_pilot_data_.csv').iloc[:5,:])


# In[62]:


def addresstoll(df):
   
    # Create empty lists for lats and lngs
    lat_list = pd.Series([])
    lng_list = pd.Series([])    
    
    # Create opener
    opener = urllib.request.FancyURLopener({})
        
    # Iterate over all rows of dataframe
    for i in range(len(df)):
        
        # Get block number (street number) and street name
        block = df['BlockNumber'][i]
        street = df['StreetName'][i]
        
        # Create url from these
        url = 'http://www.datasciencetoolkit.org/street2coordinates/'        + str(block) + '+' + str(street) + '+' + 'Charlottesville+VA'
        
        # Store webpage contents
        f = opener.open(url)
        content = f.read()
        
        # Get lat and long out of content string
        lat = re.search(r".*latitude\": *(.*?) *,\n*", str(content)).group(1)
        lng = re.search(r".*longitude\": *(.*?) *,\n*", str(content)).group(1)
        
        # Add to the lists
        lat_list[i] = lat
        lng_list[i] = lng
               
    return lat_list, lng_list
#       sys.stdout.write('\r' + str(lat) +', '+ str(lng))
#       time.sleep(0.1)


# In[64]:


crime = pd.read_csv('./data/Crime_Data.csv')


# In[66]:


crime[:5]


# In[67]:


crime_lats, crime_lngs = addresstoll(crime[:5])


# In[68]:


crime_lats


# In[69]:


crime_lngs

