from .models import Payment, Szesnastka
from .siepomaga import HandlerSiePomaga
from .youtube import YoutubeHandler


def fetch_new_payments():
    last_payment = Payment.objects.order_by('-id').first()
    if last_payment:
        last_payment_date, last_payment_id = last_payment.date, last_payment.payment_id
    else:
        last_payment_date, last_payment_id = None, None

    for batch in HandlerSiePomaga(last_payment_id, last_payment_date).run():
        Payment.objects.bulk_create(batch)
        print('Inserting...')


def fetch_new_videos():
    Szesnastka.objects.all().delete()
    videos = YoutubeHandler().run()
    Szesnastka.objects.bulk_create(videos)
