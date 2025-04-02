import datetime
import os
from flask import Flask, render_template, request
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv() #gets environment variables from .env file 


def create_app():

    app = Flask(__name__)
    client = MongoClient(os.getenv("MONGODB_URI"))#from .env file
    app.db = client.microblog


    @app.route("/", methods=["GET", "POST"])
    def home():

        if request.method == "POST":
            entry = request.form.get("content")
            formated_date = datetime.datetime.today().strftime("%Y-%m-%d")
            app.db.entries.insert_one({"content": entry, "date": formated_date })
        entries_with_date = [
            (
                entry["content"],
                entry["date"],
                datetime.datetime.strptime(entry["date"], "%Y-%m-%d").strftime("%b %d")
            )
            for entry in app.db.entries.find({})
        ]
        return render_template("home.html", entries=entries_with_date)

    return app