import datetime
import time
import requests
from requests.exceptions import HTTPError, ConnectionError

from django.core.management.base import BaseCommand, CommandError

from currency.utils import to_decimal, check_exist_and_create_rate
from currency import consts
from currency import model_choices as mch
from currency.models import Rate, Source


# class Command(BaseCommand):
#     # help = 'Get rate by rate_id and print to console'
#
#     def add_arguments(self, parser):
#         parser.add_argument('rate_ids', nargs='+', type=int)
#
#     def handle(self, *args, **options):
#         for rate_id in options['rate_ids']:
#             try:
#                 rate = Rate.objects.get(pk=rate_id)
#             except Rate.DoesNotExist:
#                 raise CommandError('Rate "%s" does not exist' % rate_id)
#
#             currency_type = rate.currency_type
#
#             self.stdout.write(self.style.SUCCESS(f'Object {rate_id} has currency_type = {currency_type}'))


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('terminate_date', nargs='+', type=datetime.date)
        parser.add_argument('retries', nargs='+', type=int)

    def handle(self, *args, **options):
        # the end date until which we parse the archive
        # terminate_date = datetime.date(2014, 7, 1)
        # terminate_date = datetime.date(2022, 9, 20)
        if options['terminate_date']:
            terminate_date = options['terminate_date']
        else:
            terminate_date = datetime.date.today() - datetime.timedelta(days=366)

        # the number of attempts to request the link in case of no response
        # retries = 3
        if options['retries']:
            retries = options['retries']
        else:
            retries = 5

        # get or create Source
        source_name = 'PrivatBank'
        source_url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
        source, created = Source.objects.get_or_create(code_name=consts.CODE_NAME_PRIVATBANK,
                                                       defaults={
                                                           'source_url': source_url,
                                                           'name': source_name,
                                                       })

        currency_type_mapper = {
            'UAH': mch.CarrencyType.CURRENCY_TYPE_UAH,
            'USD': mch.CarrencyType.CURRENCY_TYPE_USD,
            'EUR': mch.CarrencyType.CURRENCY_TYPE_EUR,
            'BTC': mch.CarrencyType.CURRENCY_TYPE_BTC,
        }

        delta_days = datetime.date.today() - terminate_date

        success_dates_counter = 0
        success_rates_counter = 0
        start = datetime.datetime.now()

        self.stdout.write(self.style.SUCCESS(f'START ARCHIVE PARSER. Datetime: {start}'))

        for i in range(delta_days.days + 1):
            on_date = datetime.date.today() - datetime.timedelta(days=i)
            date_str = on_date.strftime("%d.%m.%Y")
            archive_url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date_str}'

            self.stdout.write(archive_url)

            # ========trying to get request from server=================
            response = None
            for n in range(retries):
                try:
                    response = requests.get(archive_url)
                    # response.raise_for_status()

                    break

                except ConnectionError as conn_exc:
                    code = conn_exc.args[0]

                    if conn_exc and n < retries - 1:
                        self.stdout.write(
                            self.style.ERROR(f'ConnectionError!!! Try number: {n + 1} [{datetime.datetime.now()}]')
                        )
                        time.sleep(n * 10)
                        continue
                    else:
                        raise CommandError(f"ConnectionError!!! [{datetime.datetime.now()}],"
                                           f"Error Desc: {code}") from conn_exc

                except HTTPError as http_exc:
                    code = http_exc.response.status_code
                    # self.stdout.write(
                    #     self.style.ERROR(f'Request Error! Status Code: {code}.')
                    # )
                    if code in [429, 500, 502, 503, 504]:
                        # retry after n seconds
                        time.sleep(n)
                        continue

                    raise
            # ==========================================================

            response_data = response.json()
            if response_data['exchangeRate']:
                # pars json
                for rate_data in response_data["exchangeRate"]:

                    # skip rates without currency_type
                    if not rate_data.get("currency"):
                        continue

                    currency_type = rate_data["currency"]
                    base_currency_type = rate_data["baseCurrency"]

                    # skip unsupported currencies
                    if currency_type not in currency_type_mapper or base_currency_type not in currency_type_mapper:
                        continue

                    # convert original source currency type to our custom currency type
                    currency_type = currency_type_mapper[currency_type]
                    base_currency_type = currency_type_mapper[base_currency_type]

                    # skip rates if currency_type == base_currency_type
                    if currency_type == base_currency_type:
                        continue

                    # skip rates if has't buy or sale (only NBU)
                    if not rate_data.get("purchaseRate") or not rate_data.get("saleRate"):
                        continue

                    buy = to_decimal(rate_data['purchaseRate'])
                    sale = to_decimal(rate_data['saleRate'])

                    if check_exist_and_create_rate(on_date,
                                                   base_currency_type,
                                                   currency_type,
                                                   source,
                                                   sale,
                                                   buy):
                        success_rates_counter += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Add rate to DB: {base_currency_type}, {currency_type}, {buy, sale}')
                        )
                    else:
                        self.stdout.write('There is already a rate in the db for this date')
                success_dates_counter += 1

        finish = datetime.datetime.now()
        self.stdout.write(self.style.SUCCESS(f'SUCCESS! Start: {start} Finish: {finish}, '
                                             f'Dates processed: {delta_days.days + 1}, '
                                             f'Rates added to DB: {success_rates_counter}'))
