from googleapiclient.discovery import build
import os


class Video:
    """Класс для видео"""

    def __init__(self, video_id):
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        try:
            api_key = os.getenv('API_KEY')
            youtube = build('youtube', 'v3', developerKey=api_key)
            video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                                   id=video_id
                                                   ).execute()
            video = video_response['items'][0]
            self.title = video['snippet']['title']
            self.url = f"https://www.youtube.com/watch?v={self.video_id}"
            self.view_count = int(video['statistics']['viewCount'])
            self.like_count = int(video['statistics']['likeCount'])

        except:
            self.title = None
            self.url = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        """Выводит в консоль информацию о видео."""
        return f"{self.title}"


class PLVideo(Video):
    def __init__(self, video_id, playlist_id):
        """Класс для плейлиста"""
        super().__init__(video_id)
        self.playlist_id = playlist_id

    def __str__(self):
        """Выводит в консоль информацию о плейлисте."""
        return f"{self.title}"
