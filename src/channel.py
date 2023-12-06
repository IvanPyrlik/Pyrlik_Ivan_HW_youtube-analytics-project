import json
import os

from googleapiclient.discovery import build


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        api_key: str = os.getenv('API_KEY')
        youtube = build('youtube', 'v3', developerKey=api_key)
        # channel_id = 'UC-OVMPlMA3-YCIeg4z5z23A'  # MoscowPython
        channel_id = 'AIzaSyCvIQes6xj93ZEizTMz29Scrt7K8We1Y10'  # HighLoad Channel
        channel = youtube.channels().list(id=channel_id, part='snippet,statistics').execute()
        return printj(channel)


def printj(dict_to_print: dict) -> None:
    """Выводит словарь в json-подобном удобном формате с отступами"""
    print(json.dumps(dict_to_print, indent=2, ensure_ascii=False))

