import os
from src.channel import Channel


class Video(Channel):
    """Класс для ютуб-канала"""

    def __init__(self, video_id) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.video_id = video_id
        self.response = (self.get_service().videos().list(id=self.video_id,
                                                          part='snippet,statistics,contentDetails,topicDetails',)
                         .execute())
        self.title = self.response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/watch?v=' + self.video_id
        self.view_count = self.response['items'][0]['statistics']['viewCount']
        self.like_count = self.response['items'][0]['statistics']['likeCount']

    def __str__(self):
        return f'{self.title}'


class PLVideo(Video):
    """Класс для ютуб-канала"""

    def __init__(self, video_id, play_list_id):
        super().__init__(video_id)
        self.play_list_id = play_list_id
        self.response = self.get_service().playlistItems().list(playlistId=self.play_list_id,
                                                                part='contentDetails',
                                                                maxResults=50,).execute()
