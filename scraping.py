#%%
from flask import Flask, render_template
from flask_pymongo import PyMongo
import Mission_to_Mars
import pandas as pd
import datetime as dt
from webdriver_manager.chrome import ChromeDriverManager
# %%
app = Flask(__name__)
# %%
# Use flask_pymongo to set up mongo connection to python
# URI = URL (Similar)
# Mongo data base set up
# Before this make sure to create the instance in the console
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# %%
# Setting up home page route:
@app.route('/')
def index():
    # this will make PyMongo find 'mars' collection in our database
    mars = mongo.db.mars.find_one()
    # The return in this line of code will return an HTML template using an index.html file
    # mars=mars tells Python to use the mars collection in MongoDB
    # Return statement tells python that the function is over
    return render_template("index.html", mars=mars)

# The function above is what links our visual representation of our work, our web app, to the code that powers it
# %%
# Setting up the scraping route
@app.route("/scrape")
def scrape():
   # This variable will point to the mongo database
   mars = mongo.db.mars
   # This variable will hold the scraped data, scrape all exported from jupyter notebook
   mars_data = scraping.scrape_all()
   #updating the data base
   # we are updating data so we need an empty json that will take the place of the data we scraped -> .update(query_parameter, data, options)
   # true makes mongo create a new file if one does not exist
   mars.update({}, mars_data, upsert=True)
   # redirect when finishing scrpaing data
   return redirect('/', code=302)
# %%
if __name__ == "__main__":
    app.run()
# %%
# The browser argument tells python we will use the browser variable
def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://data-class-mars.s3.amazonaws.com/Mars/index.html'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add try/except for error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()

    except AttributeError:
        return None, None

    return news_title, news_p

def mars_facts():
    try:
        # Using the read_html pandas function to scrape the facts table into a dataframe
        df = pd.read_html('ttps://data-class-mars-facts.s3.amazonaws.com/Mars_Facts/index.html')[0]
    # BaseExpectation is used becauase we are using the read_html function and it won't handle any user defined expectations.
    # BaseExpectation will help us avoid the AttributeErrors that comes from importing a table into a df
    except BaseException:
        return

    # Assign columns and set index of dataframe
    df.columns = ['Description', 'Mars', 'Earth']
    df.set_index('Description', inplace=True)

    return df.to_html()

# The following function will initialize the browser
# It will create a data dictionary
# end the webdriver and return the scaped data
def scrape_all():
    # Initiate headless driver for deploymnet
    executable_path = {'executable_path': ChromeDriverManager().install()}

    # 2 browsers, one is the variable the other is the parameter
    # headless = False will make the scraping visible to us, if set on true you'll get the result immidiately
    browser = Browser('chrome', **executable_path, headless=True)

    # Setting up news_title and news_paragraph variables to hold the data that will be scraped
    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in dictionary
    # This dict will run all of the function created and it stores all of the results
data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "last_modified": dt.datetime.now()
}


if __name__ == "__main__":
    # If running as script, print scraped data
    print(scrape_all())