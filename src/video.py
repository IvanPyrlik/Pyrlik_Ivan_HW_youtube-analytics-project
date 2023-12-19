import os

from googleapiclient.discovery import build


class Video:

    def __init__(self, video_id: str) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API."""
        self.__video_id = video_id
        self.video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
        self.video_title = self.video['items'][0]['snippet']['title']
        self.video_url = f'https://youtu.be/{self.__video_id}'
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']

    def __str__(self):
        return self.video_title

    @classmethod
    def get_service(cls):
        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        return youtube


class PLVideo(Video):

    def __init__(self, video_id: str, playlist_id: str) -> None:
        """Экземпляр инициализируется id плейлиста. Дальше все данные будут подтягиваться по API."""
        super().__init__(video_id)
        self.__video_id = video_id
        self.video = self.get_service().videos().list(part='snippet,statistics,contentDetails,topicDetails', id=video_id).execute()
        self.video_title = self.video['items'][0]['snippet']['title']
        self.video_url = f'https://youtu.be/{self.__video_id}'
        self.view_count = self.video['items'][0]['statistics']['viewCount']
        self.like_count = self.video['items'][0]['statistics']['likeCount']
        self.playlist_id = playlist_id

