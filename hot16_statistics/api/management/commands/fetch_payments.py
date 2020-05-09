from django.core.management import BaseCommand

from api.tasks import fetch_new_payments


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        fetch_new_payments()
