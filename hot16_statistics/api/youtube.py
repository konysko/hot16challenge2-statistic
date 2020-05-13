import logging
from datetime import datetime
from typing import List

import googleapiclient.discovery
import googleapiclient.errors
from django.conf import settings
from django.utils import timezone
from django.utils.timezone import make_aware

from .models import Szesnastka

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


class YoutubeHandler:
    api_service_name = "youtube"
    api_version = "v3"
    key = settings.YT_API_KEY
    payload = {
        'playlistId': 'PLJracTP7uCLI3Lh1egh8xo6eJNwJIoIUW',
        'maxResults': 50,
        'part': 'snippet, contentDetails'
    }
    forbidden_titles = ['Deleted video', 'Private video']

    def __init__(self):
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=self.key
        ).playlistItems()

    def run(self):
        request = self.youtube.list(**self.payload)
        page = request.execute()
        parsed_videos = []
        while page:
            parsed_videos.extend(self.update_videos(page['items']))
            request = self.youtube.list_next(previous_request=request, previous_response=page)
            if not request:
                break
            page = request.execute()
        return parsed_videos

    @classmethod
    def update_videos(cls, videos: List[dict]):
        parsed_videos = []
        for video in videos:
            if video['snippet']['title'] in cls.forbidden_titles:
                continue
            parsed_video = cls.parse_video(video)
            parsed_videos.append(parsed_video)

        logger.info(f'Added {len(parsed_videos)} videos')
        return parsed_videos

    @staticmethod
    def parse_video(video: dict) -> Szesnastka:
        details = video['contentDetails']
        snippet = video['snippet']
        if date := details.get('videoPublishedAt', '')[:-1]:
            parsed_date = make_aware(timezone.datetime.fromisoformat(date))
        else:
            parsed_date = None
        return Szesnastka(
            video_id=details['videoId'],
            published_at=parsed_date,
            title=snippet['title'],
            description=snippet['description'],
            video_url=f'https://www.youtube.com/watch?v={details["videoId"]}',
            thumbnail=snippet['thumbnails']['high']['url']
        )
