from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from helper import apology
import requests

app = Flask(__name__)
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    else:
        if request.form.get('twitch-button') == "Twitch":
            channel = request.form.get("channel-name")
            global response
            response = requests.get(f"https://pwn.sh/tools/streamapi.py?url=twitch.tv/{channel}").json()
            response_parse = str(response["urls"].keys()).replace("dict_keys(", "").replace(")", "").replace("'audio_only', ", "").replace("'", "")
            return render_template("index.html", resolution=response_parse.strip("[]").split(", "), channel=channel)
        elif request.form.get("twitch-channel") == "Twitch-Channel":
            resolution = request.form.get("resolution")
            link = response["urls"][resolution]
            return render_template("twitch.html", link=link)
        else:
            link = request.form.get("video-link")
            if "youtube" in link:
                return render_template("youtube.html", link=link.replace("watch?v=", "embed/")+"?autoplay=1")
            else:
                return render_template("youtube.html", link="https://youtube.com/embed/"+link+"?autoplay=1")
            

def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)

for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

if __name__ == "__main__":
    app.run(host="localhost")