import os
from googleapiclient.discovery import build

api_key: str = str(os.getenv('API_KEY'))
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id



    def print_info(self) -> None:
        """Выводит в консоль информацию о канале."""

        youtube = build('youtube', 'v3', developerKey=api_key)
        response = youtube.channels().list(part='snippet,statistics', id=self.channel_id).execute()

        if 'items' in response:
            channel_data = response['items'][0]
            title = channel_data['snippet']['title']
            description = channel_data['snippet']['description']
            view_count = channel_data['statistics']['viewCount']
            subscriber_count = channel_data['statistics']['subscriberCount']
            video_count = channel_data['statistics']['videoCount']

            print(f"Название канала: {title}")
            print(f"Описание: {description}")
            print(f"Количество просмотров: {view_count}")
            print(f"Количество подписчиков: {subscriber_count}")
            print(f"Количество видео: {video_count}")
        else:
            print("Канал не найден.")
