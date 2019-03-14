#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import Dependencies
import os
import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
from selenium import webdriver
import requests
import time


# In[2]:


# Use requests and BeautifulSoup to scrape Nasa News for latest news
url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
response = requests.get(url)
soup = bs(response.text, 'lxml')
# print(soup.prettify())


# In[3]:


results = soup.find('div', class_='features')
# for result in results:
#     print(result)


# In[4]:


news_title = results.find('div', class_='content_title').text
newsp = results.find('div', class_='rollover_description').text
print(news_title)
print(newsp)


# In[6]:


# Find image url for current featured mars image
executable_path = {'executable_path': r'/Users/Kamil/Downloads\/chromedriver'}
browser = Browser('chrome', **executable_path, headless=False)

nasa_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(nasa_url)

nasa_html = browser.html
nasa_soup = bs(nasa_html, "lxml")


# In[7]:


featured = nasa_soup.find('div', class_='default floating_text_area ms-layer')
featured_image = featured.find('footer')
featured_image_url = 'https://www.jpl.nasa.gov'+ featured_image.find('a')['data-fancybox-href']
print(str(featured_image_url))


# In[8]:


# Scrape Mars Weather Twitter account for latest weather report on Mars
twitter_url = 'https://twitter.com/marswxreport?lang=en'
twitter_response = requests.get(twitter_url)
twitter_soup = bs(twitter_response.text, 'lxml')
twitter_result = twitter_soup.find('div', class_='js-tweet-text-container')
# for tweet in twitter_result:
#     print(tweet)


# In[9]:


mars_weather = twitter_result.find('p', class_='js-tweet-text').text
mars_weather


# In[10]:


# Scrape space-facts.com for mars fact using Pandas read_html function
mars_facts_url = 'https://space-facts.com/mars/'
tables = pd.read_html(mars_facts_url)
tables


# In[11]:


# Create pandas dataframe
df = tables[0]
df.columns = ['Description', 'Value']
df.head()


# In[12]:


# Reset index 
df.set_index('Description', inplace=True)
df.head()


# In[13]:


# Export pandas df to html script
mars_facts = df.to_html()
mars_facts.replace("\n", "")
df.to_html('mars_facts.html')


# In[14]:


# Scrape astrogeology.usgs.gov for hemisphere image urls and titles
hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(hemisphere_url)

hemisphere_html = browser.html
hemisphere_soup = bs(hemisphere_html, 'lxml')
base_url ="https://astrogeology.usgs.gov"

image_list = hemisphere_soup.find_all('div', class_='item')

# Create list to store dictionaries of data
hemisphere_image_urls = []

# Loop through each hemisphere and click on link to find large resolution image url
for image in image_list:
    hemisphere_dict = {}
    
    href = image.find('a', class_='itemLink product-item')
    link = base_url + href['href']
    browser.visit(link)
    
    time.sleep(1)
    
    hemisphere_html2 = browser.html
    hemisphere_soup2 = bs(hemisphere_html2, 'lxml')
    
    img_title = hemisphere_soup2.find('div', class_='content').find('h2', class_='title').text
    hemisphere_dict['title'] = img_title
    
    img_url = hemisphere_soup2.find('div', class_='downloads').find('a')['href']
    hemisphere_dict['url_img'] = img_url
    
    # Append dictionary to list
    hemisphere_image_urls.append(hemisphere_dict)
      
hemisphere_image_urls

