import logging
import re
from concurrent.futures.process import ProcessPoolExecutor
from datetime import datetime
from typing import Tuple, List

import requests
from bs4 import BeautifulSoup

from .models import Payment

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
logger = logging.getLogger(__name__)


class ConnectionSiePomaga:
    next_payment_url = 'https://www.siepomaga.pl/skarbonki/hot16challenge'
    data_pattern = re.compile(r'var data = \"(.*)\"\nvar refresh', re.DOTALL)
    next_url_pattern = re.compile(r'/skarbonki/hot16challenge(.*)\\\"')
    headers = {
        'accept': 'text/javascript, application/javascript, application/ecmascript, application/x-ecmascript, */*; q=0.01',
        'x-requested-with': 'XMLHttpRequest'
    }
    next_url = ''

    def get_next_page(self):
        while True:
            url = f'{self.next_payment_url}{self.next_url}'
            logger.info(f'Fetching page {url}')
            raw_page = requests.get(url, headers=self.headers)
            logger.info(f'Fetched page with status code: {raw_page.status_code}')
            page = self._get_parsed_page(raw_page)
            yield BeautifulSoup(page, 'html.parser')

            self.next_url = self._get_next_url(page)
            if not self.next_url:
                return

    def _get_next_url(self, parsed_page):
        groups = self.next_url_pattern.search(parsed_page).groups()
        if not groups:
            return
        return groups[0].replace(';', '&')

    def _get_parsed_page(self, raw_page):
        return self.data_pattern.search(
            raw_page.text
        ).groups()[0].replace(
            '\\\'', ''
        ).replace(
            '\\/', '/'
        ).replace(
            '\\n', '\n'
        )


class HandlerSiePomaga:

    def __init__(self, last_payment_id: str, last_payment_date: str):
        self.handler = ConnectionSiePomaga()
        self.last_payment_id = last_payment_id
        self.last_payment_date = last_payment_date
        self.payments = []

    def run(self):
        payments_num = 0
        for page in self.handler.get_next_page():
            try:
                payments, is_last = self.parse_page(page)
                self.payments.extend(payments)
                payments_num += len(payments)

                logger.info(f'Last payment on {payments[-1].date}')
                logger.info(f'Got {len(self.payments)} payments')

            except Exception:
                continue

            if payments_num % 720 == 0 or is_last:
                yield self.payments
                self.payments = []

    def parse_page(self, page) -> Tuple[List[Payment], bool]:
        parsed_payments = []
        for payment in page.find_all('div', 'sp-payment'):
            parsed_payment, is_last = self.parse_payment(payment)
            if is_last:
                return parsed_payments, True
            parsed_payments.append(parsed_payment)
        return parsed_payments, False

    def parse_payment(self, payment) -> Tuple[Payment, bool]:
        date = payment.find('small')['data-time']
        parsed_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S%z')
        parsed_id = payment['id'].lstrip('payment-')
        is_last = bool(parsed_id == self.last_payment_id and parsed_date == self.last_payment_date)
        amount = payment.find('strong').text.strip().rstrip(' zł').replace(',', '.').replace(' ', '')
        return Payment(
            payment_id=parsed_id,
            author=payment.find('h4').text.strip(),
            comment=payment.find('div', 'sp-payment-comment').text.strip(),
            date=date,
            parsed_date=parsed_date,
            amount=0.0 if amount == 'X' else float(amount)
        ), is_last
