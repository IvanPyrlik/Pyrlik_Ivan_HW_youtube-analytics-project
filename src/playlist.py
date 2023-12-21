import datetime
import os

import isodate
from googleapiclient.discovery import build


class PlayList:

    def __init__(self, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        self.playlist_id = playlist_id
        self.playlists = self.get_service().playlists().list(id=playlist_id, part='snippet', maxResults=50).execute()
        for playlist in self.playlists['items']:
            self.title = playlist['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.playlist_id}'
        self.playlists_video = self.get_service().playlistItems().list(playlistId=playlist_id, part='contentDetails',
                                                                       maxResults=50, ).execute()
        video_ids: list[str] = [video['contentDetails']['videoId'] for video in self.playlists_video['items']]
        self.video_response = (
            self.get_service().videos().list(
                part='contentDetails,statistics',
                id=','.join(video_ids)).execute())

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube

    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста.
        """
        total_duration = datetime.timedelta()
        for video in self.video_response['items']:
            # YouTube video duration is in ISO 8601 format
            iso_8601_duration = video['contentDetails']['duration']
            duration = isodate.parse_duration(iso_8601_duration)
            total_duration += duration
        return total_duration

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).
        """
        likes_list = []
        for video in self.video_response['items']:
            likes_list.append(video['statistics']['likeCount'])
        max_likes_video = max(likes_list)
        for video in self.video_response['items']:
            if max_likes_video == video['statistics']['likeCount']:
                return f'https://youtu.be/{video['id']}'
