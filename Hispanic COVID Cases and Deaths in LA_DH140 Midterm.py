#!/usr/bin/env python
# coding: utf-8

# # Midterm Notebook 

# Annalise Gutierrez

# # Research Question 

# How has COVID-19 imapcted people of different demogrpahic backgrounds and what could be possible reasons why?

# # Importing Libraries and Data Sources

# In[2]:


import urllib.request, json
import pandas as pd 
import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt
import contextily as ctx 
import osmnx as ox
import os
import plotly.express as px
from sodapy import Socrata 


# In[3]:


#state policy 
statepolicy = pd.read_csv('state_policy_data.csv')

#covid data by race and ethnicity 
covid_eth = pd.read_csv('covid_data_by_race_ethnicity.csv')

#LA Times COVID data by race/ethnicity
latimes_eth = pd.read_csv('https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/cdph-race-ethnicity.csv')

#LA Times COVID data by place
latimes_place = pd.read_csv('https://raw.githubusercontent.com/datadesk/california-coronavirus-data/master/latimes-place-totals.csv')

#LA hispanic census data
gdf_his = gpd.read_file('acs2019_5yr_B03002_14000US06037534001.geojson')

#LA occupation census data 
gdf_occ = gpd.read_file('acs2019_5yr_C24050_14000US06037534001.geojson')


# # Data Analysis: State Policy 

# In[4]:


statepolicy.shape


# In[5]:


statepolicy.sample()


# In[6]:


list(statepolicy)


# In[7]:


statepolicy.policy_type.value_counts()


# In[8]:


statepolicy_typecount = statepolicy.policy_type.value_counts().reset_index()
statepolicy_typecount


# In[9]:


statepolicy_typecount = statepolicy_typecount.rename(columns={'index':'policy','policy_type':'count'})
statepolicy_typecount


# In[10]:


statepolicy_typecount.plot.barh(figsize=(12,6),
                               x='policy',
                               title="Policy Types in the United States")


# In[11]:


statepolicy_typecount = statepolicy_typecount.sort_values(by='count', ascending=True)
statepolicy_typecount


# In[12]:


statepolicy_typecount[-10:].plot.barh(figsize=(12,4),
                               x='policy',
                                y='count',
                               title="Top 10 Policy Types in the United States")


# In[13]:


statepolicy[statepolicy['state_id']=='CA'].head()


# In[14]:


statepolicy_CA = statepolicy[statepolicy['state_id']=='CA']
statepolicy_CA


# In[15]:


statepolicy_CA.policy_type.value_counts()


# In[16]:


statepolicyCA_typecount = statepolicy_CA.policy_type.value_counts().reset_index()
statepolicyCA_typecount


# In[17]:


statepolicyCA_typecount = statepolicyCA_typecount.rename(columns={'index':'policy','policy_type':'count'})
statepolicyCA_typecount


# In[18]:


statepolicyCA_typecount = statepolicyCA_typecount.sort_values(by='count', ascending=True)
statepolicyCA_typecount


# In[19]:


statepolicyCA_typecount[-10:].plot.barh(figsize=(12,4),
                               x='policy',
                                y='count',
                               title="Top 10 Policy Types in the California")


# # Data Analysis: COVID Cases and Deaths by Ethnicity 

# In[20]:


covid_eth.shape


# In[21]:


covid_eth.info()


# In[22]:


list(covid_eth)


# In[23]:


covid_eth[covid_eth['State']=="CA"]


# In[24]:


covid_ethCA = covid_eth[covid_eth['State']=="CA"]
covid_ethCA


# In[25]:


list(covid_ethCA)


# In[36]:


columns_keeping = ['State',
 'Cases_Total',
 'Cases_White',
 'Cases_Latinx',
 'Deaths_Total',
 'Deaths_White',
 'Deaths_Latinx',]


# In[37]:


covid_ethCA = covid_ethCA[columns_keeping]
covid_ethCA


# In[38]:


covid_ethCA.shape


# In[44]:


covid_ethCA['Cases Percent White'] = covid_ethCA['Cases_White']/covid_ethCA['Cases_Total']*100
covid_ethCA['Cases Percent Latinx'] = covid_ethCA['Cases_Latinx']/covid_ethCA['Cases_Total']*100
covid_ethCA['Deaths Percent White'] = covid_ethCA['Deaths_White']/covid_ethCA['Deaths_Total']*100
covid_ethCA['Deaths Percent Latinx'] = covid_ethCA['Deaths_Latinx']/covid_ethCA['Deaths_Total']*100
covid_ethCA


# In[40]:


covid_ethCA.plot(figsize = (10,5))


# In[42]:


covid_ethCA.plot.bar(stacked=True)


# # Data Analysis: LA Times COVID Data by Race and Ethnicity 

# In[45]:


latimes_eth.head()


# In[46]:


latimes_eth.shape


# In[47]:


list(latimes_eth)


# In[49]:


latimes_eth = latimes_eth.sort_values(by=["date"],ascending=True)
latimes_eth


# In[50]:


latimes_eth.tail(40)


# In[51]:


latimes_eth.groupby("race").confirmed_cases_total.describe()


# In[54]:


temp = latimes_eth.query("race == ['white', 'latino', 'black', 'asian', 'other']")
px.bar(temp,
      x='date',
      y='confirmed_cases_total',
      color='race',
      title="Confirmed Cases by Race and Ethnicity in Los Angeles")


# In[55]:


latimes_ethmean = latimes_eth.confirmed_cases_total.mean()
latimes_ethmean


# In[59]:


px.scatter(latimes_eth,
          x='date',
          y='race',
          color='confirmed_cases_total',
          size='confirmed_cases_total',
          size_max=40,
          hover_name='race',
          animation_frame='date',
          color_continuous_scale = 'RdYlGn_r',
          range_color=(0,latimes_ethmean*2))


# # Data Analysis: LA Times COVID Data by Place

# In[60]:


latimes_place.head()


# In[61]:


list(latimes_place)


# In[62]:


latimes_place.shape


# In[66]:


latimes_place = latimes_place.sort_values(by=["date"], ascending=True)
latimes_place


# In[67]:


latimes_place.tail(40)


# In[68]:


latimes_place.info()


# In[69]:


latimes_place.place.value_counts()


# In[71]:


centralLA = latimes_place.query("place==['Gardena', 'Carson', 'Compton', 'Beverly Hills', 'Santa Monica']")
px.bar(centralLA, 
      x='date',
      y='confirmed_cases',
      color='place')


# In[73]:


latimes_place_mean = latimes_place.confirmed_cases.mean()
latimes_place_mean


# In[74]:


px.scatter(latimes_place,
          x='x',
          y='y',
          color='confirmed_cases',
          size='confirmed_cases',
          size_max=40,
          hover_name='place',
          animation_frame='date',
          color_continuous_scale = 'RdYlGn_r',
          range_color=(0,latimes_place_mean*2))


# In[1]:


fig = px.scatter_geo(latimes_place,
          lon='x',
          lat='y',
          color='confirmed_cases',
          size='confirmed_cases',
          size_max=40,
          hover_name='place',
          animation_frame='date',
          color_continuous_scale = 'RdYlGn_r',
          range_color=(0,latimes_place_mean*2))

fig.update_geos(fitbounds="locations")


# In[ ]:




