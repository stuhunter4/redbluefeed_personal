from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_news

# Create an instance of Flask
app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/rednews_app")

# Route to render index.html template using data from Mongo
@app.route("/")
def home():
    
    new_listings = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", news=new_listings)

# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():
    
    # run the scrape function and save the results to a varialbe
    news_data = scrape_news.scrape_info()

    # update the mongo database using update and upsert=True
    mongo.db.collection.update({}, news_data, upsert=True)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)