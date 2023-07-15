import os
from googleapiclient.discovery import build
from datetime import timedelta


api_key: str = str(os.getenv('API_KEY'))
youtube = build('youtube', 'v3', developerKey=api_key)

class PlayList:

    def __init__(self,id):
        self.id = id
        playlist_response = youtube.playlists().list(
            part='snippet',
            id=self.id
        ).execute()
        self.title = playlist_response['items'][0]['snippet']['title']
        self.url = f'https://www.youtube.com/playlist?list={self.id}'
        playlist_videos = youtube.playlistItems().list(playlistId=self.id,
                                                       part='contentDetails',
                                                       maxResults=50,
                                                       ).execute()
        video_ids = [video['contentDetails']['videoId'] for video in playlist_videos['items']]
        video_response = youtube.videos().list(part='contentDetails,statistics',
                                               id=','.join(video_ids)
                                               ).execute()
        self.__videos = video_response['items']

    @property
    def total_duration(self):
        total_duration = timedelta()
        for video in self.__videos:
            duration = video.get('contentDetails').get('duration')
            video_duration = self.parse_duration(duration)
            total_duration += video_duration
        return total_duration

    @staticmethod
    def parse_duration(duration: str) -> timedelta:
        parts = duration.split('T')
        time_part = parts[1]
        hours = int(time_part.split('H')[0]) if 'H' in time_part else 0
        minutes = int(time_part.split('M')[0].split('H')[-1]) if 'M' in time_part else 0
        seconds = int(time_part.split('S')[0].split('M')[-1]) if 'S' in time_part else 0
        video_duration = timedelta(hours=hours, minutes=minutes, seconds=seconds)
        return video_duration

    def show_best_video(self) -> str:
        best_video = max(self.__videos, key=lambda video: video.get('statistics').get('likeCount'))
        video_id = best_video.get('id')
        return f'https://youtu.be/{video_id}'
