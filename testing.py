from pytube import YouTube

url = "https://www.youtube.com/watch?v=kpDRMD25GEI"
yt = YouTube(url)
streams = yt.streams

print(streams)