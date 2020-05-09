from rest_framework import serializers


class StatisticSerializer(serializers.Serializer):
    date = serializers.DateTimeField()
    video_titles = serializers.ListField(
        serializers.CharField()
    )
    video_thumbnails = serializers.ListField(
        serializers.CharField()
    )
    video_urls = serializers.ListField(
        serializers.CharField()
    )
    total_sum_amount = serializers.FloatField()
