from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_data"
mongo = PyMongo(app)

@app.route("/")
def index():
    mars_data = mongo.db.mars_data.find_one()
    return render_template("index.html", mars_data = mars_data)

@app.route("/scrape")
def scraper():
    mars_data = mongo.db.mars_data
    mars_dict = scrape_mars.scrape()
    mars_data.update_one({}, {"$set": mars_dict}, upsert=True)
    return redirect("/", code = 302)

if __name__ == "__main__":
    app.run(debug=True)
