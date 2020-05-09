import logging
from datetime import datetime
from typing import List

import googleapiclient.discovery
import googleapiclient.errors
from django.utils import timezone
from django.utils.timezone import make_aware

from .models import Szesnastka

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


class YoutubeHandler:
    api_service_name = "youtube"
    api_version = "v3"
    key = 'AIzaSyC7u6_eTH7Bf1TdvbZrI8Mglvb2zrIdFtM'
    payload = {
        'playlistId': 'PL5T2bKQEuT6B9QtbQMILHNEks-vRO1Pv3',
        'maxResults': 50,
        'part': 'snippet, contentDetails'
    }

    def __init__(self):
        self.youtube = googleapiclient.discovery.build(
            self.api_service_name, self.api_version, developerKey=self.key
        ).playlistItems()

    def run(self):
        request = self.youtube.list(**self.payload)
        page = request.execute()
        while page:
            self.update_videos(page['items'])
            request = self.youtube.list_next(previous_request=request, previous_response=page)
            if not request:
                break
            page = request.execute()

    @classmethod
    def update_videos(cls, videos: List[dict]):
        parsed_videos = []
        for video in videos:
            parsed_video = cls.parse_video(video)
            if not Szesnastka.objects.filter(video_id=parsed_video.video_id).exists():
                parsed_videos.append(parsed_video)

        Szesnastka.objects.bulk_create(parsed_videos)
        logger.info(f'Added {len(parsed_videos)} videos')

    @staticmethod
    def parse_video(video: dict) -> Szesnastka:
        details = video['contentDetails']
        snippet = video['snippet']
        parsed_date = make_aware(timezone.datetime.fromisoformat(details['videoPublishedAt'][:-1]))
        return Szesnastka(
            video_id=details['videoId'],
            published_at=parsed_date,
            title=snippet['title'],
            description=snippet['description'],
            video_url=f'https://www.youtube.com/watch?v={details["videoId"]}',
            thumbnail=snippet['thumbnails']['high']['url']
        )
