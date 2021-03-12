# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd

# Set the executable path and initialize the chrome browser in splinter
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

url = 'https://mars.nasa.gov/news/'
browser.visit(url)
# Optional delay for loading the page
# This code will help us search for elements with specific combination of tag ul and li and attribute item_list and slide
# it also tells the browser to wait 1 second before loading the page
slide_elem = browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

# Setting up HTML parser
# Before you parse we need a parent variable to filter
# slide_elem is looking for the <ul/> tag and <li />
# slide_elem is our parent element that we will use to filter further our search
html = browser.html
news_soup = soup(html, 'html.parser')
slide_elem = news_soup.select_one('ul.item_list li.slide')

# scrapping begins
slide_elem.find('div', class_='content_title').text

# Use the parent element to find the first `a` tag and save it as `news_title`
# .get_text() = .text
news_title = slide_elem.find("div", class_='content_title').get_text()
news_title

# Use the parent element to find the first `a` tag and save it as `news_title`
# .find() -> gives one summary
# .find_all() -> gives all summaries - all tags are searched
news_text = slide_elem.find("div", class_= 'article_teaser_body').get_text()
news_text


# Image scraping
# Visit URL
url = 'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/index.html'
browser.visit(url)

# Find and click the full image button
# There are several buttons but we want the full image, do ctrl f and see what # of button it is
full_image_elem = browser.find_by_tag('button')[1]
full_image_elem.click()

# Parse the resulting html with soup
html = browser.html
img_soup = soup(html, 'html.parser')

# Find the realtive image url
# get('src') = pulls the link to the image
img_url_rel = img_soup.find('img', class_ = 'fancybox-image').get('src')
img_url_rel

img_url = f'https://data-class-jpl-space.s3.amazonaws.com/JPL_Space/{img_url_rel}'
img_url


# Mars Table
# Using pandas read html to get the mars table
df = pd.read_html('https://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
df.columns=['description', 'Mars', 'Earth']
df.set_index('description', inplace=True)
df

df.to_html()

browser.quit()