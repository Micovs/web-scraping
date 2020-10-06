from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/MarsDB"
mongo = PyMongo(app)


@app.route("/")
def index():
    data = mongo.db.data.find_one()
    return render_template("index.html", data = data)


@app.route("/scrape")
def scraper():
    data = mongo.db.data
    Mars_data = scrape_mars.scrape()
    data.update({}, Mars_data, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
