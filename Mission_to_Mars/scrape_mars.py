#!/usr/bin/env python
# coding: utf-8

# In[1]:


# This will be your webscraping code
# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import pandas as pd
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo


# In[50]:


# initialize Pymongo 
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# In[53]:


db = client.mars_mission_db
db


# In[4]:


executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)


# In[9]:


# Nasa Mars URL
url = 'https://mars.nasa.gov/news/'
#browser visit
browser.visit(url)
html = browser.html

soup = BeautifulSoup(html,'html.parser')


# In[25]:


# News Title and News Paragraph fetching. 
#news_title
results = soup.find_all('div', class_='content_title')[4].text
news_title = results.strip('\n\n')
news_title


# In[24]:


#news_p 
news_p = soup.find_all('div', class_='rollover_description_inner')[9].text
news_p = news_p.strip('\n\n')
news_p


# In[34]:


# Vist the JPL Space Images Site for some scrapping
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)

browser.click_link_by_id('full_image')


# In[35]:


html = browser.html
soup = BeautifulSoup(html,'html.parser')


# In[38]:


featured_image_url = soup.article.a['data-fancybox-href']
featured_image_url = (f'https://www.jpl.nasa.gov{featured_image_url}')
featured_image_url                      


# In[39]:


# Mars Facts Table Scrapping
# url for webpage
url = 'https://space-facts.com/mars/'
# use Pandas read_html
mars_table = pd.read_html(url)
mars_table


# In[42]:


# Convert to DF set columns
mars_table.columns=['Information','Mars']
mars_table


# In[43]:


# Convert Table to HTML string for app loading. 
mars_table_html = mars_table.to_html()
mars_table_html


# In[44]:


# USGS Hemisphere high res photo scrapping
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[48]:


# set up empty list for hemisphere dic info
hemisphere_url_dic = []
for i in range(4):
    browser.find_by_css('a.product-item h3')[i].click()
    soup = BeautifulSoup(browser.html,'html.parser')
    
    #try block to append info
    try:
        title = soup.find('h2', class_='title').get_text()
        image = soup.find('a', text = 'Sample' ).get('href')
    except AttributeError:
        title = None
        image = None
        
    hemisphere_image = {
        "title": title,
        "image_url": image
    }
    #append
    hemisphere_url_dic.append(hemisphere_image)
    #get browser back to main page
    browser.back()


# In[49]:


# print list of dictionaries
hemisphere_url_dic


# In[ ]:




