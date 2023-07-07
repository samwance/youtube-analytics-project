import os
from googleapiclient.discovery import build
import json


api_key: str = str(os.getenv('API_KEY'))
youtube = build('youtube', 'v3', developerKey=api_key)

class Channel:
    """Класс для ютуб-канала"""


    def __init__(self, channel_id: str) -> None:
        """Экземпляр инициализируется id канала. Дальше все данные будут подтягиваться по API."""
        self.channel_id = channel_id
        self.youtube = self.get_service().channels().list(id=self.channel_id, part='snippet,statistics').execute()
        self.name = self.youtube['items'][0]['snippet']['title']
        self.description = self.youtube['items'][0]['snippet']['description']
        self.link = f"https://www.youtube.com/channel/{self.channel_id}"
        self.subscriber_count = int(self.youtube['items'][0]['statistics']['subscriberCount'])
        self.video_count = int(self.youtube['items'][0]['statistics']['videoCount'])
        self.view_count = int(self.youtube['items'][0]['statistics']['viewCount'])


    def __str__(self):
        return f"{self.name} ({self.link})"

    def __add__(self, other):
        return int(self.subscriber_count) + int(other.subscriber_count)


    def __sub__(self, other):
        return int(self.subscriber_count) - int(other.subscriber_count)


    def __gt__(self, other):
        return self.subscriber_count > other.subscriber_count


    def __ge__(self, other):
        return self.subscriber_count >= other.subscriber_count


    def __lt__(self, other):
        return self.subscriber_count < other.subscriber_count


    def __le__(self, other):
        return self.subscriber_count <= other.subscriber_count


    def __eq__(self, other):
        return self.subscriber_count == other.subscriber_count

    @classmethod
    def get_service(cls):
        """Возвращает объект службы YouTube API для выполнения запросов к API."""
        return build('youtube', 'v3', developerKey=api_key)

    def to_json(self, file_path: str) -> None:
        """
               Сохраняет информацию о канале в JSON-файл.
        """
        channel_data = {
            'channel_id': self.channel_id,
            'channel_name': self.name,
            'channel_description': self.description,
            'channel_link': self.link,
            'subscriber_count': self.subscriber_count,
            'video_count': self.video_count,
            'view_count': self.view_count
        }
        with open(file_path, 'w') as file:
            json.dump(channel_data, file, indent=2, ensure_ascii=False)


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
