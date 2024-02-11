import os
from src.channel import Channel


class Video(Channel):
    """Класс для ютуб-канала"""

    def __init__(self, video_id) -> None:
        """Экземпляр инициализируется id видео. Дальше все данные будут подтягиваться по API.

        :param video_id: 'ID' видео.
        :param response: Словарь с информацией по видео.
        :param title: Название видео.
        :param url: Ссылка на видео.
        :param view_count: Количество просмотров.
        :param like_count: Количество лайков на видео.
        """
        self.video_id = video_id
        self.response = self.get_service().videos().list(id=self.video_id,
                                                         part='snippet,statistics').execute()
        try:
            self.title = self.response['items'][0]['snippet']['title']
            self.url = 'https://www.youtube.com/watch?v=' + self.video_id
            self.view_count = self.response['items'][0]['statistics']['viewCount']
            self.like_count = self.response['items'][0]['statistics']['likeCount']

        except IndexError:
            self.title = None
            self.view_count = None
            self.like_count = None

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    """Класс для ютуб-канала"""

    def __init__(self, video_id, play_list_id):
        super().__init__(video_id)
        self.play_list_id = play_list_id
        self.response = self.get_service().playlistItems().list(playlistId=self.play_list_id,
                                                                part='contentDetails',
                                                                maxResults=50).execute()
