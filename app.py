#%%
from flask import Flask, render_template
from flask_pymongo import PyMongo
import Mission_to_Mars
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
    return render_template("index.html", mars=mars)

# The function above is what links our visual representation of our work, our web app, to the code that powers it
# %%
