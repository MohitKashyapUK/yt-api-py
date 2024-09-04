from flask import Flask, request, jsonify
from urllib.parse import urlparse
from markupsafe import escape
from pytube import YouTube

app = Flask(__name__)

@app.route('/')
def index():
    return f"<h1>{escape("/<URL or ID>")}</h1>"

@app.route('/<path:uri>')
def hello_world(uri):
    video_id = request.args.get('v', None)
    if not video_id:
        path = urlparse(uri).path
    # yt = YouTube(url)
    return uri