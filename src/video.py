from googleapiclient.discovery import build
import os


api_key: str = str(os.getenv('API_KEY'))
youtube = build('youtube', 'v3', developerKey=api_key)


class Video:


    def __init__(self, id_video):
        self.id_video = id_video
        video_response = youtube.videos().list(part='snippet,statistics,contentDetails,topicDetails',
                                               id=self.id_video
                                               ).execute()
        self.video_title = video_response['items'][0]['snippet']['title']
        self.link = f"https://youtu.be/{self.id_video}"
        self.view_count = video_response['items'][0]['statistics']['viewCount']
        self.like_count = video_response['items'][0]['statistics']['likeCount']


    def __str__(self):
        return self.video_title


class PLVideo(Video):
    def __init__(self, id_video, id_playlist):
        super().__init__(id_video)
        self.id_playlist = id_playlist
