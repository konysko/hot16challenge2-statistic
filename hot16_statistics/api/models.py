import json

from django.contrib.postgres.fields import ArrayField
from django.db import models, connection

from api.serializers import StatisticSerializer


class Payment(models.Model):
    payment_id = models.CharField(max_length=256, unique=True)
    author = models.CharField(max_length=512)
    comment = models.CharField(max_length=512, blank=True, null=True)
    date = models.CharField(max_length=512)
    parsed_date = models.DateTimeField(db_index=True)
    amount = models.FloatField()


class Szesnastka(models.Model):
    video_id = models.CharField(max_length=2048, unique=True)
    title = models.TextField()
    description = models.TextField()
    thumbnail = models.URLField()
    video_url = models.URLField()
    published_at = models.DateTimeField(db_index=True)


class StatisticView(models.Model):
    class Meta:
        managed = False
        db_table = 'api_statistic_view'

    id = models.IntegerField(primary_key=True)
    ids = ArrayField(
        models.IntegerField()
    )  # Payment ids
    video_titles = ArrayField(
        models.TextField()
    )
    video_thumbnails = ArrayField(
        models.URLField()
    )
    video_urls = ArrayField(
        models.URLField()
    )
    total_sum_amount = models.DecimalField(max_digits=10, decimal_places=2)
    hour = models.IntegerField()
    day = models.IntegerField()
    month = models.IntegerField()
    date = models.DateTimeField()

    @staticmethod
    def refresh_view():
        with connection.cursor() as cursor:
            cursor.execute('''
                DROP MATERIALIZED VIEW IF EXISTS api_statistic_view;
                CREATE MATERIALIZED VIEW api_statistic_view
                AS
                SELECT P.MONTH,
                       P.DAY,
                       P.HOUR,
                       P.TOTAL_SUM_AMOUNT,
                       F.VIDEO_URLS,
                       F.VIDEO_THUMBNAILS,
                       F.VIDEO_TITLES,
                       P.IDS::int[],
                       row_number() OVER () AS ID,
                       to_timestamp(
                       '2019' || '-' || P.MONTH::text || '-' || P.DAY::text || ' ' || P.HOUR::text || ':' || '00' || '00' , 
                       'YYYY-MM-DD HH24:MI:SS'
                       ) AS DATE
                FROM (
                         SELECT MONTH,
                                DAY,
                                HOUR,
                                SUM(SUM(SUM_AMOUNT)) OVER (ORDER BY MONTH, DAY, HOUR) AS TOTAL_SUM_AMOUNT,
                                IDS
                         FROM (
                                  SELECT EXTRACT(MONTH FROM parsed_date) AS MONTH,
                                         EXTRACT(DAY FROM parsed_date)   AS DAY,
                                         EXTRACT(HOUR FROM parsed_date)  AS HOUR,
                                         SUM(amount)                     AS SUM_AMOUNT,
                                         array_agg(id)                   AS IDS
                                  FROM api_payment
                                  GROUP BY MONTH, DAY, HOUR
                              ) AS P

                         GROUP BY MONTH, DAY, HOUR, IDS
                ) AS P
                LEFT JOIN (
                    SELECT EXTRACT(MONTH FROM published_at) AS MONTH,
                           EXTRACT(DAY FROM published_at)   AS DAY,
                           EXTRACT(HOUR FROM published_at)  AS HOUR,
                           array_agg(video_url)             AS VIDEO_URLS,
                           array_agg(thumbnail)             AS VIDEO_THUMBNAILS,
                           array_agg(title)                 AS VIDEO_TITLES
                    FROM api_szesnastka
                    GROUP BY MONTH, DAY, HOUR
                ) F ON F.MONTH = P.MONTH AND F.DAY = P.DAY AND F.HOUR = P.HOUR;
            ''')

    @staticmethod
    def export_json(queryset=None, name=None):
        if not queryset:
            queryset = StatisticView.objects.values('date', 'video_titles', 'video_thumbnails', 'video_urls',
                                                    'total_sum_amount')
        if not name:
            name = '/tmp/statistic.json'
        with open(name, 'w') as handler:
            serializer_data = StatisticSerializer(queryset, many=True).data
            json.dump(serializer_data, handler)
            return True
