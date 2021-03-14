#!/usr/bin/env python
# coding: utf-8

# In[5]:


# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd


# In[6]:


# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[7]:


# Visit the mars nasa news site
url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
# This code will help us search for elements with specific combination of tag ul and li and attribute item_list and slide
# it also tells the browser to wait 1 second before loading the page
slide_elem = browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)


# In[8]:


# Setting up HTML parser
# Before you parse we need a parent variable to filter
# slide_elem is looking for the <ul/> tag and <li />
# slide_elem is our parent element that we will use to filter further our search
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')


# In[9]:


# scrapping begins
slide_elem.find('div', class_='content_title').text


# In[10]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# .get_text() = .text
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title


# In[11]:


# Use the parent element to find the first `a` tag and save it as `news_title`
# .find() -> gives one summary
# .find_all() -> gives all summaries - all tags are searched
news_text = slide_elem.find("div", class_= 'article_teaser_body').get_text()
news_text


# Image scraping

# In[12]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[13]:


# Find and click the full image button
# There are several buttons but we want the full image, do ctrl f and see what # of button it is
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[14]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')


# In[15]:


# Find the realtive image url 
# get('src') = pulls the link to the image
img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
img_url_rel


# In[16]:


img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# Mars Table

# In[17]:


# Using pandas read html to get the mars table
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df


# In[18]:


df.to_html()


# In[19]:


# Set the executable path and initialize Splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# ### Visit the NASA Mars News Site

# In[20]:


# Visit the mars nasa news site
url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
browser.visit(url)

# Optional delay for loading the page
browser.is_element_present_by_css('div.list_text', wait_time=1)


# In[21]:


# Convert the browser html to a soup object and then quit the browser
html = browser.html
news_soup = soup(html, 'html.parser')

slide_elem = news_soup.select_one('div.list_text')


# In[22]:


slide_elem.find('div', class_='content_title')


# In[23]:


# Use the parent element to find the first a tag and save it as `news_title`
news_title = slide_elem.find('div', class_='content_title').get_text()
news_title


# In[24]:


# Use the parent element to find the paragraph text
news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
news_p


# ## JPL Space Images Featured Image

# In[25]:


# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)


# In[26]:


# Find and click the full image button
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()


# In[27]:


# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')
img_soup


# In[28]:


# find the relative image url
img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
img_url_rel


# In[29]:


# Use the base url to create an absolute url
img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# # Mars Facts

# In[30]:


df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.head()


# In[31]:


df.columns=['Description', 'Mars', 'Earth']
df.set_index('Description', inplace=True)
df


# In[32]:


df.to_html()


# ## D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles

# ## Hemispheres

# In[33]:


# 1. Use browser to visit the URL 
url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[34]:


# 2. Create a list to hold the images and titles.
hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
html = browser.html
html_soup = soup(html, 'html.parser')
hemi_elements = html_soup.find_all('div', class_='description')

for element in hemi_elements:
    # Create an empty dictionary
    hemisphere = {}
    
    # Navigate to the full-resolution image
    image_ref_link = element.find('a', class_='itemLink product-item')
    image_link = f"https://astrogeology.usgs.gov{image_ref_link.get('href')}"
    browser.visit(image_link) 
    
    # Retrieve the full-resolution image url and title
    full_image_url = browser.links.find_by_text('Sample')['href']
    title = browser.find_by_tag('h2').text
    
    # Add the url and title to the dictionary
    hemisphere = {'img_url': full_image_url, 'title' : title}
    hemisphere_image_urls.append(hemisphere)


# In[35]:


# 4. Print the list that holds the dictionary of each image url and title.
hemisphere_image_urls


# In[36]:


# 5. Quit the browser
browser.quit()


# In[ ]:




