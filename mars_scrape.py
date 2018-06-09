
# coding: utf-8

# In[1]:


# import dependencies
from bs4 import BeautifulSoup
from splinter import Browser
import requests
import os
import time
from selenium import webdriver


# In[2]:


# use Selenium to scrape html from Nasa's Mars homepage
chromedriver = 'chromedriver.exe'
os.environ["webdriver.chrome.driver"] = chromedriver
driver = webdriver.Chrome(chromedriver)
driver.get('https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest')
time.sleep(5)
html = driver.page_source
soup = BeautifulSoup(html, 'lxml')


# In[3]:


# find article headers by searching by class
newsTitle = soup.find('div', class_='content_title')
title = newsTitle.text
newsTeaser = soup.find('div', class_='article_teaser_body')
teaser = newsTeaser.text
print(title + " - " + teaser)


# In[4]:


executable_path = {'executable_path': './chromedriver'}
browser = Browser('chrome', **executable_path)
url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[5]:


browser.click_link_by_id('full_image')


# In[6]:


#locate featured image in browser html
html = browser.html
soup = BeautifulSoup(html, 'lxml')
topImage = soup.find('img', class_='fancybox-image')
topImage


# In[7]:


# generate string for featured image URL
topImageUrl = "https://www.jpl.nasa.gov" + topImage['src']
print("Featured Image URL: "+topImageUrl)


# In[8]:


# pull text from latest tweet
browser.visit("https://twitter.com/marswxreport?lang=en")
html = browser.html
soup = BeautifulSoup(html, 'lxml')
latestWeather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
latestWeather


# In[10]:


# read stat table from Mars fact website
import pandas as pd
marsTables = pd.read_html("https://space-facts.com/mars/")
marsTables


# In[11]:


# make dataframe of results, save as html
df = marsTables[0]
df.columns = ["","Stat"]
df.set_index('', inplace=True)
df.to_html('marsTable.html')


# In[12]:


# select hemisphere items from homepage
browser.visit("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
html = browser.html
soup = BeautifulSoup(html, 'lxml')
hemis = soup.find_all('div', class_='item')
hemis


# In[23]:


# for each item in homepage, follow its link to retrieve the full-size jpg url of the hemisphere image
hemiPics = []
for hemi in hemis:
    a = hemi.find('a', class_= 'itemLink product-item')
    url = 'https://astrogeology.usgs.gov'+a['href']
    name = hemi.find('h3').text
    browser.visit(url)
    
    html = browser.html
    picSoup = BeautifulSoup(html, 'lxml')
    fullPic = picSoup.find('img', class_='wide-image')
    picURL = 'https://astrogeology.usgs.gov' + fullPic['src']
    picPair = {'name':name, 'img_url':picURL}
    hemiPics.append(picPair)
hemiPics

