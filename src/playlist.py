from googleapiclient.discovery import build
from datetime import timedelta  # Импорт модуля datetime
import isodate
import os


class PlayList:
    """Класс для плейлиста"""

    def __init__(self, playlist_id):
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlists = youtube.playlists().list(
            part='snippet',
            id=playlist_id
        ).execute()
        self.title = playlists['items'][0]['snippet']['title']
        self.url = f"https://www.youtube.com/playlist?list={self.playlist_id}"

    def __str__(self) -> str:
        """Выводит в консоль информацию о плейлисте."""
        return f"{self.title}"

    def __repr__(self) -> str:
        """Выводит в консоль информацию о плейлисте."""
        return f"{self.title}"

    @property
    def total_duration(self) -> timedelta:
        """Выводит в консоль информацию об общей длительности плейлиста."""
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlists_videos = youtube.playlistItems().list(
            part='contentDetails',
            playlistId=self.playlist_id,
            maxResults=50).execute()

        video_ids = []

        for video in playlists_videos['items']:
            video_ids.append(video['contentDetails']['videoId'])

        video_response = youtube.videos().list(
            part='contentDetails,statistics',
            id=','.join(video_ids)).execute()

        total_duration = timedelta()
        for item in video_response['items']:
            if 'duration' in item['contentDetails']:
                iso_8601_duration = item['contentDetails']['duration']
                duration = isodate.parse_duration(iso_8601_duration)
                total_duration += duration
        return total_duration

    def show_best_video(self):
        """Выводит в консоль информацию о самом лучшем видео."""
        api_key = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        playlist_videos = youtube.playlistItems().list(playlistId=self.playlist_id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        current_video_likes = 0
        for video_id in video_ids:
            video_response = youtube.videos().list(part='contentDetails,statistics',
                                                   id=video_id).execute()
            if int(video_response['items'][0]['statistics']['likeCount']) > current_video_likes:
                current_video_likes = int(video_response['items'][0]['statistics']['likeCount'])
            else:
                continue
        return f"https://youtu.be/{video_id}"
