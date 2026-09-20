import yt_dlp

class Youtube:
    @staticmethod
    def search(name, n = 1):
        ydl_opts = {
            'quiet': True,         
            'skip_download': True,  
        }

        search_query = f"ytsearch{n}:{name}"

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            try:
                info = ydl.extract_info(search_query, download=False)
            except: # TODO: Return A Error Here To Display
                return None 

            if 'entries' in info and info['entries']:
                return info['entries']
            else:
                return None 

    @staticmethod
    def fetch(url):
        ydl_opts = {
            "skip_download": True,
            "format": "bestaudio/best",
            "quiet": True                
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            
            title = info.get("title")
            artist = info.get("uploader")
            duration = info.get("duration_string")
            thumbnail = info.get("thumbnail")
            audio_url = info.get("url")
            
            print(f"Title: {title}")
            print(f"Audio Stream URL: {audio_url}")
            
            return {
                "title": title,
                "artist": artist,
                "duration": duration,
                "thumbnail": thumbnail,
                "url": audio_url
            }
