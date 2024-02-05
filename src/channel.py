import os
from googleapiclient.discovery import build
import json


class Channel:
    """Класс для ютуб-канала"""
    # os.environ["API_KEY"] = 'AIzaSyBzAZejRuPV61GONeULcMt_w9aI5e1gmK8'
    api_key: str = os.getenv('API_KEY')

    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.__channel_id = channel_id

        self.response = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        self.title = self.response['items'][0]['snippet']['title']
        self.description = self.response['items'][0]['snippet']['description']
        self.url = 'https://www.youtube.com/channel/' + channel_id
        self.subscriber_count = int(self.response['items'][0]['statistics']['subscriberCount'])
        self.video_count = self.response['items'][0]['statistics']['videoCount']
        self.view_count = self.response['items'][0]['statistics']['viewCount']

    def __str__(self):
        return f'{self.title} ({self.url})'

    def __add__(self, other):
        return self.subscriber_count + other.subscriber_count

    def __sub__(self, other):
        return self.subscriber_count - other.subscriber_count

    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count

    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count

    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""
        response = Channel.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        print(json.dumps(response, indent=2, ensure_ascii=False))

    def to_json(self, file_name):
        """Получает данные о канале, записывает их в словарь и создает '.json file' с этим словарем."""
        response = self.get_service().channels().list(id=self.__channel_id, part='snippet,statistics').execute()
        to_json_dict = json.dumps(response, indent=2, ensure_ascii=False)

        to_json = open(file_name, 'w', encoding='UTF=8')
        to_json.write(to_json_dict)

    @classmethod
    def get_service(cls):
        """Возвращающий объект для работы с YouTube API"""
        return build('youtube', 'v3', developerKey=Channel.api_key)

    @property
    def channel_id(self):
        """Получаем возможность обращаться к '__channel_id' вне класса"""
        return self.__channel_id

    @channel_id.setter
    def channel_id(self, channel_id):
        """Вносим изменения в '__channel_id'"""
        self.__channel_id = channel_id
