from src.channel import Channel
import json
from datetime import timedelta
import isodate


class PlayList(Channel):
    """Класс для вывода информации по play-list из 'Youtube'"""
    def __init__(self, play_list_id):
        """Экземпляр инициализируется id play-list из 'Youtube'. Дальше все данные будут подтягиваться по API.

        :param play_list_id: 'ID' play-list.
        :param response: Словарь с информацией по play-list.
        :param title: Название play-list.
        :param url: Ссылка на play-list.
        """
        self.play_list_id = play_list_id
        self.response = self.get_service().playlists().list(id=play_list_id, part='snippet',).execute()
        self.title = self.response['items'][0]['snippet']['title']
        self.url = 'https://www.youtube.com/playlist?list=' + self.play_list_id

    def info(self):
        print(json.dumps(self.response, indent=2, ensure_ascii=False))

    @property
    def total_duration(self):
        """
        Возвращает объект класса datetime.timedelta с суммарной длительность плейлиста.
        :retutn: Суммарноая длительность плейлиста.
        """
        response = self.get_service().playlistItems().list(playlistId=self.play_list_id,
                                                           part='snippet,contentDetails',
                                                           maxResults=50).execute()
        time_all_videos: timedelta = timedelta(hours=0, minutes=0)

        for item in range(0, response['pageInfo']['totalResults']):
            video_id = response['items'][item]['snippet']['resourceId']['videoId']
            response_video_id = self.get_service().videos().list(id=video_id,
                                                                 part='contentDetails').execute()
            time_videos = response_video_id['items'][0]['contentDetails']['duration']
            duration = isodate.parse_duration(time_videos)
            time_all_videos += duration

        return time_all_videos

    def show_best_video(self):
        """
        Возвращает ссылку на самое популярное видео из плейлиста (по количеству лайков).
        :return: Самое популярное видео из плейлиста.
        """
        response = self.get_service().playlistItems().list(playlistId=self.play_list_id,
                                                           part='snippet,contentDetails',
                                                           maxResults=50).execute()
        max_like_count = 0
        url = ''

        for item in range(0, response['pageInfo']['totalResults']):
            video_id = response['items'][item]['snippet']['resourceId']['videoId']
            response_video_id = self.get_service().videos().list(id=video_id,
                                                                 part='snippet,statistics').execute()

            if int(response_video_id['items'][0]['statistics']['likeCount']) > max_like_count:
                max_like_count = int(response_video_id['items'][0]['statistics']['likeCount'])
                url = "https://youtu.be/" + video_id

        return url
