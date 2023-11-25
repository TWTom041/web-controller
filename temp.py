import vlc
import yt_dlp
import re
import time

rick_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
ffmpeg_options = {'options': '-vn'}
ydl_opts = {'format': 'bestaudio'}
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    song_info = ydl.extract_info(rick_url, download=False)

stream_url = song_info['url']
print(stream_url)

pattern = rf'expire=(?P<value>[^&]+)'
result = re.search(pattern, stream_url)
print(result.group('value'))


Instance = vlc.Instance()
player = Instance.media_player_new()
Media = Instance.media_new(stream_url)
Media.get_mrl()
player.set_media(Media)
player.play()

time.sleep(10)