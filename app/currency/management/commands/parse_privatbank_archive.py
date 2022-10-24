import datetime
import time
import requests
from requests.exceptions import HTTPError, ConnectionError

from django.core.management.base import BaseCommand

from currency.utils import to_decimal, check_exist_and_create_rate
from currency import consts
from currency import model_choices as mch
from currency.models import Rate, Source


class Command(BaseCommand):

    # ===========PARSER SETTINGS=================

    # path and name log file
    log_file_name = 'app/currency/management/commands/parse_privatbank_archive_log.txt'

    # begin from date, comment/uncomment what do you need
    # start_date = datetime.date(2014, 7, 22)
    start_date = datetime.date.today()

    # number of retries when there is no connection
    connection_retries = 20  # set number of attempts

    # number of retries when response.status_code in [429, 500, 502, 503, 504]
    response_retries = 10  # set number of attempts

    # number of attempts (steps) back by archive dates, if response_data['exchangeRate'] is empty
    response_data_retries = 10  # set number of attempts

    # delay in seconds after each parsing iteration
    delay_sec = 3

    # maximum number of parser iterations (useful when testing)
    max_parser_iterations = 10000

    def add_line_to_log(self, line_text: str, write_mode: str = "a", out_to_terminal: bool = False):
        """
        function create log-file and write row to end
        :param line_text: text that will be displayed in the log and in the terminal
        :param write_mode: if "w" - rewrite file, if "a" - append row to end of file (by default = "a")
        :param out_to_terminal: show message to terminal (by default = False)
        :return:
        """
        f = open(self.log_file_name, write_mode)
        f.write(f"{datetime.datetime.utcnow()} - {line_text}\n")
        f.close()
        if out_to_terminal:
            self.stdout.write(line_text)

    def handle(self, *args, **options):

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

        # initial number of records in Rate
        initial_rates_count = Rate.objects.count()

        connection_condition = True  # current connection condition
        connection_attempt = 0  # current connection iteration

        response_condition = True  # current response condition
        response_attempt = 0  # current response iteration

        response_data_condition = True  # current response_data condition
        response_data_attempt = 0  # current response_data iteration

        delta_days = 0

        self.add_line_to_log('START!!!!', 'w', True)

        while connection_condition and response_condition and response_data_condition:
            on_date = self.start_date - datetime.timedelta(days=delta_days)
            date_str = on_date.strftime("%d.%m.%Y")
            archive_url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={date_str}'
            self.add_line_to_log(archive_url)
            # response = None
            try:
                response = requests.get(archive_url)
                connection_condition = True
                connection_attempt = 0

                response.raise_for_status()
                response_condition = True
                response_attempt = 0

                self.add_line_to_log(f'Connection OK! Response code: {response.status_code}\n')

                # ==========pars json==========================
                response_data = response.json()
                if response_data['exchangeRate']:
                    response_data_condition = True
                    response_data_attempt = 0

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

                        # skip rates if has not buy or sale (only NBU)
                        if not rate_data.get("purchaseRate") or not rate_data.get("saleRate"):
                            continue

                        buy = to_decimal(rate_data['purchaseRate'])
                        sale = to_decimal(rate_data['saleRate'])
                        self.add_line_to_log(f'Rate: {base_currency_type}, {currency_type}, {buy, sale}')

                        if check_exist_and_create_rate(on_date,
                                                       base_currency_type,
                                                       currency_type,
                                                       source,
                                                       sale,
                                                       buy):
                            self.add_line_to_log(f'Add rate to DB! \n')
                        else:
                            self.add_line_to_log(f'There is already a rate in the db for this date.\n')
                else:
                    if response_data_attempt <= self.response_data_retries:
                        self.add_line_to_log(f'This date has no rates!!! Attempt:{response_data_attempt}.\n')
                        response_data_attempt += 1
                    else:
                        response_data_condition = False
                        self.add_line_to_log(f'Looks like it is the end, Baby!!! Exit!!!\n')
                # ===============================================

                delta_days += 1
                time.sleep(self.delay_sec)

            except ConnectionError as conn_exc:
                if connection_attempt <= self.connection_retries:
                    self.add_line_to_log(f'ConnectionError!!! Attempt:{connection_attempt}.\n')
                    connection_attempt += 1
                    time.sleep(connection_attempt * 60)
                else:
                    connection_condition = False
                    self.add_line_to_log(f'ConnectionError!!! Exit!!!\n{conn_exc.args}\n')

            except HTTPError as http_exc:
                code = http_exc.response.status_code
                if code in [429, 500, 502, 503, 504]:
                    if response_attempt <= self.response_retries:
                        self.add_line_to_log(f'ResponseError!!! Status: {code}. Attempt:{connection_attempt}.\n')
                        response_attempt += 1
                        time.sleep(response_attempt * 30)
                    else:
                        response_condition = False
                        self.add_line_to_log(f'ResponseError!!! Status: {code}. Exit!!!\n')

            # exit from parser by limit of iterations
            if delta_days == self.max_parser_iterations:
                connection_condition = False
                self.add_line_to_log(f'The parser has reached the limit: {self.max_parser_iterations}', 'a', True)

        # final number of records in Rate
        end_rates_count = Rate.objects.count()
        # added number of records in Rate
        added_rates_count = end_rates_count - initial_rates_count

        self.add_line_to_log(f'THE END!!! Added rates: {added_rates_count}', 'a', True)
