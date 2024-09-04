# from urllib.parse import urlparse
from flask import Flask, Response, request
from markupsafe import escape
import yt_dlp, cv2

app = Flask(__name__)

def get_frame_as_image(url, timestamp_ms):
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
    """
    Return:
        int: miliseconds
    """
    parts = duration.split(":")
    obj = [1, 60, 3600, 86400]
    seconds = 0

    parts.reverse()
    for index, value in enumerate(parts): seconds += int(value) * obj[index]
    return seconds * 1000

@app.route('/')
def index():
    return f"<h1>{escape("/<URL or ID>")}</h1>"

@app.route('/screenshot')
def capture_screenshot():
    url = request.args.get('url')
    duration = int(request.args.get('duration', 0))  # Example timestamp in milliseconds
    timestamp_ms = isoFormatToMS(duration)

    if not url: return Response("URL is required.", 500)
    elif not timestamp_ms: return Response("MS is required.", 500)

    ydl_opts = {
        'format': 'bestvideo*[height<=1080]',  # Aap yahan format change kar sakte hain
        'noplaylist': True,
        'quiet': True,
        'outtmpl': '-',  # Stream output directly
    }
    video_url = None

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Get video info
        info_dict = ydl.extract_info(url, download=False)
        videoUrl = info_dict.get('url')

        if not videoUrl: return Response("Something is wrong.", 500)

        video_url = videoUrl

    image_data = get_frame_as_image(video_url, timestamp_ms)

    if image_data is None: return Response("Could not capture the frame", status=500)

    # Return the image data as a response
    return Response(image_data, mimetype='image/png')

@app.route('/<path:uri>')
def yt(uri):
    url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
    ydl_opts = {
        'format': 'bestvideo*',  # Aap yahan format change kar sakte hain
        'noplaylist': True,
        'quiet': True,
        'outtmpl': '-',  # Stream output directly
    }

    video_url = None

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Get video info
        info_dict = ydl.extract_info(url, download=False)
        videoUrl = info_dict.get('url')
        if not videoUrl: return "Something is wrong."
        video_url = videoUrl
    
    return video_url