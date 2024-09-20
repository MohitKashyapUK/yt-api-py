# from urllib.parse import urlparse
from flask import Flask, Response, request, jsonify, send_file
from html import escape
from urllib.parse import urlparse
import yt_dlp

app = Flask(__name__)

""" def get_frame_as_image(url, timestamp_ms):
    cap = cv2.VideoCapture(url)

    if not cap.isOpened(): return None

    cap.set(cv2.CAP_PROP_POS_MSEC, timestamp_ms)

    ret, frame = cap.read()

    if not ret: return None

    # frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Convert the frame to PNG format
    _, buffer = cv2.imencode('.png', frame)
    image_data = buffer.tobytes()

    cap.release()
    return image_data

def isoFormatToMS(duration):
    '''
    Return:
        int: miliseconds
    '''
    parts = duration.split(":")
    obj = [1, 60, 3600, 86400]
    seconds = 0

    parts.reverse()
    for index, value in enumerate(parts): seconds += int(value) * obj[index]
    return seconds * 1000 """

def yt_video_details(url):
    ydl_opts = {
        'format': 'bestvideo*[height<=1080][protocol^=http]',  # Aap yahan format change kar sakte hain
        'noplaylist': True,
        'cookiefile': 'cookies.txt',
        'quiet': True,
        'outtmpl': '-',  # Stream output directly
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Get video info
        info_dict = ydl.extract_info(url, download=False)

        return info_dict

@app.route('/')
def index():
    return f"<h1>{escape('/<URL or ID>')}</h1>"

"""@app.route('/screenshot')
def capture_screenshot():
    url = request.args.get('url')
    duration = request.args.get('duration', 0)  # Example timestamp in milliseconds
    timestamp_ms = isoFormatToMS(duration)

    if not url: return Response("URL is required.", status=500)
    elif not timestamp_ms: return Response("MS is required.", status=500)

    # Get video details and extract the video URL
    info_dict = yt_video_details(url)
    video_url = info_dict.get('url')

    if not video_url: return Response("Something is wrong.", status=500)

    image_data = get_frame_as_image(video_url, timestamp_ms)

    if image_data is None: return Response("Could not capture the frame", status=500)

    # Return the image data as a response
    return Response(image_data, mimetype='image/png')"""

@app.route('/favicon.ico')
def favicon():
    return send_file('favicon.png')

@app.route('/testing/<path:url>')
def test(url):
    id = request.args.get('v')

    if not id:
        # return jsonify(urlparse(url))
        path = urlparse(url).path
        arr = path.split('/')

        if not path.startswith('/'): id = path
        elif path.startswith('/shorts'): id = arr[2]
        elif path.startswith('/live'): id = arr[2]
        else: id = arr[1]

        if id.startswith('@') or id == 'channel': return 'Please give video URL.'

    return id

@app.route('/<path:uri>')
def yt(uri):
    id = request.args.get('v')

    # Parsing URL
    if not id:
        # return jsonify(urlparse(url))
        path = urlparse(uri).path
        arr = path.split('/')

        if not path.startswith('/'): id = path
        elif path.startswith('/shorts'): id = arr[2]
        elif path.startswith('/live'): id = arr[2]
        else: id = arr[1]

        if id.startswith('@') or id == 'channel': return Response('Please give video URL.', status=500)

    # Main code
    try:
        url = 'https://www.youtube.com/watch?v=' + id # YouTube video URL
        info_dict = yt_video_details(url) # YouTube video's details and formats

        if request.args.get("get_url"): return info_dict.url

        return jsonify(info_dict["formats"])
    except Exception as e:
        return Response(str(e), status=500)