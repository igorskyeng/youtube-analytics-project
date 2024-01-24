import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        api_key = 'AIzaSyBzAZejRuPV61GONeULcMt_w9aI5e1gmK8'
        self.channel_id = channel_id
        self.youtube = build('youtube', 'v3', developerKey=api_key)

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = self.youtube.channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))

