from celery import shared_task
import requests
from settings import settings
from django.core.mail import send_mail
from time import sleep
from bs4 import BeautifulSoup

from currency.utils import to_decimal, check_and_create_rate
from currency import consts
from currency import model_choices as mch

# helpful console commands:

# запустить celery worker с выводом лога в консоль
# cd app && celery -A settings worker --loglevel=INFO

# запустить celery beat с выводом лога в консоль
# cd app && celery -A settings beat --loglevel=INFO

# запустить celery worker с очисткой очереди заданий без блокирования окна консоли (detach)
# cd app && celery -A settings worker --purge -D

# запустить celery beat без блокирования окна консоли (detach)
# cd app && celery -A settings beat --detach

# Показать все планировщики celery
# ps -ef | grep celery

# Завершить все задачи и планирощик celery
# pkill -9 -f tasks.updates.celery
# или так
# cd app && celery -A tasks.updates.celery control shutdown


# @shared_task
# def slow_func():
#     print('START')
#     sleep(3)
#     print('END')


@shared_task
def send_contact_us_email(subject, email_from):
    body = f"""
    Subject From Client: {subject}
    Email: {email_from}
    Wants to contact
    """
    sleep(10)
    send_mail(
        subject,
        body,
        settings.EMAIL_HOST_USER,
        [settings.EMAIL_HOST_USER],
        fail_silently=False,
    )


@shared_task
def parse_privatbank():
    """
    Parser task for api privatbank. If Rate is new - add object to db
    :return: None
    """
    from currency.models import Source

    source_name = 'PrivatBank'
    # card rate
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'

    # cash rate
    # url = 'https://api.privatbank.ua/p24api/pubinfo?json&exchange&coursid=5'

    # get_or_create (if source object is not exist -> create it)
    # if created == True object was created, if created == False object was get from db
    source, created = Source.objects.get_or_create(code_name=consts.CODE_NAME_PRIVATBANK,
                                                   defaults={
                                                       'source_url': url,
                                                       'name': source_name,
                                                   })

    currency_type_mapper = {
        'UAH': mch.CarrencyType.CURRENCY_TYPE_UAH,
        'USD': mch.CarrencyType.CURRENCY_TYPE_USD,
        'EUR': mch.CarrencyType.CURRENCY_TYPE_EUR,
        'BTC': mch.CarrencyType.CURRENCY_TYPE_BTC,
    }

    response = requests.get(url)
    response.raise_for_status()  # raise error if not OK
    response_data = response.json()

    # pars json
    for rate_data in response_data:
        currency_type = rate_data['ccy']
        base_currency_type = rate_data['base_ccy']

        # skip unsupported currencies
        if currency_type not in currency_type_mapper or base_currency_type not in currency_type_mapper:
            continue

        # convert original source currency type to our custom currency type
        currency_type = currency_type_mapper[currency_type]
        base_currency_type = currency_type_mapper[base_currency_type]

        buy = to_decimal(rate_data['buy'])
        sale = to_decimal(rate_data['sale'])

        check_and_create_rate(base_currency_type, currency_type, source, sale, buy)


@shared_task
def parse_monobank():
    """
    Parser task for api monobank. If Rate is new - add object to db
    :return: None
    """
    from currency.models import Source

    source_name = 'MonoBank'
    url = 'https://api.monobank.ua/bank/currency'

    # get_or_create (if source object is not exist -> create it)
    # if created == True object was created, if created == False object was get from db
    source, created = Source.objects.get_or_create(code_name=consts.CODE_NAME_MONOBANK,
                                                   defaults={
                                                       'source_url': url,
                                                       'name': source_name,
                                                   })

    currency_type_mapper = {
        '980': mch.CarrencyType.CURRENCY_TYPE_UAH,
        '840': mch.CarrencyType.CURRENCY_TYPE_USD,
        '978': mch.CarrencyType.CURRENCY_TYPE_EUR,
    }

    response = requests.get(url)
    response.raise_for_status()  # raise error if not OK
    response_data = response.json()

    # pars json
    for rate_data in response_data:
        currency_type = str(rate_data['currencyCodeA'])
        base_currency_type = str(rate_data['currencyCodeB'])

        # skip unsupported currencies
        if currency_type not in currency_type_mapper or base_currency_type not in currency_type_mapper:
            continue

        # convert original source currency type to our custom currency type
        currency_type = currency_type_mapper[currency_type]
        base_currency_type = currency_type_mapper[base_currency_type]

        buy = to_decimal(rate_data['rateBuy'])
        sale = to_decimal(rate_data['rateSell'])

        check_and_create_rate(base_currency_type, currency_type, source, sale, buy)


@shared_task
def parse_vkurse():
    """
    Parser task for api 'vkurse.dp.ua'. If Rate is new - add object to db
    :return: None
    """
    from currency.models import Source

    source_name = 'VKurse'
    url = 'http://vkurse.dp.ua/course.json'

    # get_or_create (if source object is not exist -> create it)
    # if created == True object was created, if created == False object was get from db
    source, created = Source.objects.get_or_create(code_name=consts.CODE_NAME_VKURSE,
                                                   defaults={
                                                       'source_url': url,
                                                       'name': source_name,
                                                   })

    # in this parser base_currency_type is always UAH
    base_currency_type = mch.CarrencyType.CURRENCY_TYPE_UAH

    currency_type_mapper = {
        'Dollar': mch.CarrencyType.CURRENCY_TYPE_USD,
        'Euro': mch.CarrencyType.CURRENCY_TYPE_EUR,
    }

    response = requests.get(url)
    response.raise_for_status()  # raise error if not OK
    response_data = response.json()

    # pars json
    for key, rate_data in response_data.items():
        currency_type = key

        # skip unsupported currencies
        if currency_type not in currency_type_mapper:
            continue

        # convert original source currency type to our custom currency type
        currency_type = currency_type_mapper[currency_type]

        buy = to_decimal(rate_data['buy'])
        sale = to_decimal(rate_data['sale'])

        check_and_create_rate(base_currency_type, currency_type, source, sale, buy)


@shared_task
def parse_oschadbank():
    """
    Parser task for html oschadbank. If Rate is new - add object to db
    :return: None
    """
    from currency.models import Source

    source_name = 'OschadBank'
    url = 'https://www.oschadbank.ua/currency-rate'

    # get_or_create (if source object is not exist -> create it)
    # if created == True object was created, if created == False object was get from db
    source, created = Source.objects.get_or_create(code_name=consts.CODE_NAME_OSCHADBANK,
                                                   defaults={
                                                       'source_url': url,
                                                       'name': source_name,
                                                   })

    # in this parser base_currency_type is always UAH
    base_currency_type = mch.CarrencyType.CURRENCY_TYPE_UAH

    currency_type_mapper = {
        'USD': mch.CarrencyType.CURRENCY_TYPE_USD,
        'EUR': mch.CarrencyType.CURRENCY_TYPE_EUR,
    }

    response = requests.get(url)
    response.raise_for_status()  # raise error if not OK

    # create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # parsing html
    div_tables = soup.find('div', attrs={'class': 'heading-block-currency-rate__tables'})
    div_not_active = div_tables.find('div', attrs={'class': 'heading-block-currency-rate__tables-scroll',
                                                   'style': 'display:none;'})
    div_tables_wrap = div_not_active.find('div', attrs={'class': 'heading-block-currency-rate__tables-wrap'})
    table = div_tables_wrap.find('table', attrs={'class': 'heading-block-currency-rate__table'})
    tbody = table.find('tbody', attrs={'class': 'heading-block-currency-rate__table-body'})
    tr_list = tbody.findAll('tr', attrs={'class': 'heading-block-currency-rate__table-row'})

    for tr in tr_list:
        td_list = tr.find_all('td', attrs={'class': 'heading-block-currency-rate__table-col'})
        currency_type = td_list[1].find('span').text

        # skip unsupported currencies
        if currency_type not in currency_type_mapper:
            continue

        # convert original source currency type to our custom currency type
        currency_type = currency_type_mapper[currency_type]

        buy = to_decimal(td_list[3].find('span').text)
        sale = to_decimal(td_list[4].find('span').text)

        check_and_create_rate(base_currency_type, currency_type, source, sale, buy)


@shared_task
def parse_creditdnepr():
    """
    Parser task for html creditdnepr. If Rate is new - add object to db
    :return: None
    """
    from currency.models import Source

    source_name = 'CreditDnipro'
    url = 'https://creditdnepr.com.ua/currency'

    # get_or_create (if source object is not exist -> create it)
    # if created == True object was created, if created == False object was get from db
    source, created = Source.objects.get_or_create(code_name=consts.CODE_NAME_CREDITDNEPR,
                                                   defaults={
                                                       'source_url': url,
                                                       'name': source_name,
                                                   })

    currency_type_mapper = {
        'UAH': mch.CarrencyType.CURRENCY_TYPE_UAH,
        'USD': mch.CarrencyType.CURRENCY_TYPE_USD,
        'EUR': mch.CarrencyType.CURRENCY_TYPE_EUR,
    }

    response = requests.get(url)
    response.raise_for_status()  # raise error if not OK

    # create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # pars html
    div_site_content = soup.find('div', attrs={'class': 'site-content'})
    div_table_overlay = div_site_content.find('div', attrs={'class': 'table-overlay'})
    table = div_table_overlay.find('table')
    tbody = table.find('tbody')
    tr_list = tbody.findAll('tr')

    for tr in tr_list:
        if tr['class'] == ['num-row', 'odd']:
            continue

        td_list = tr.find_all('td')
        currency_type = td_list[0].text.strip().split("/")[0]
        base_currency_type = td_list[0].text.strip().split("/")[1]

        # skip unsupported currencies
        if currency_type not in currency_type_mapper or base_currency_type not in currency_type_mapper:
            continue

        # convert original source currency type to our custom currency type
        currency_type = currency_type_mapper[currency_type]
        base_currency_type = currency_type_mapper[base_currency_type]

        buy = to_decimal(td_list[1].text)
        sale = to_decimal(td_list[2].text)

        check_and_create_rate(base_currency_type, currency_type, source, sale, buy)


@shared_task
def parse_creditagricole():
    """
    Parser task for html ukrgasbank. If Rate is new - add object to db
    :return: None
    """
    from currency.models import Source

    source_name = 'CreditAgricole'
    url = 'https://credit-agricole.ua/kurs-valyut'

    # get_or_create (if source object is not exist -> create it)
    # if created == True object was created, if created == False object was get from db
    source, created = Source.objects.get_or_create(code_name=consts.CODE_NAME_CREDITAGRICOLE,
                                                   defaults={
                                                       'source_url': url,
                                                       'name': source_name,
                                                   })

    # in this parser base_currency_type is always UAH
    base_currency_type = mch.CarrencyType.CURRENCY_TYPE_UAH

    currency_type_mapper = {
        'USD': mch.CarrencyType.CURRENCY_TYPE_USD,
        'EUR': mch.CarrencyType.CURRENCY_TYPE_EUR,
    }

    response = requests.get(url)
    response.raise_for_status()  # raise error if not OK

    # create BeautifulSoup object
    soup = BeautifulSoup(response.text, 'html.parser')

    # pars html
    section = soup.find('section', attrs={'class': 'exchange-rates-page'})
    div_container = section.find('div', attrs={'class': 'container'})
    div_data_list = div_container.find_all('div')
    for div_el in div_data_list:
        if div_el.attrs.get('data-list') == '2':
            div_table = div_el.find('div', attrs={'class': 'exchange-rates-table'})
            div_rows_list = div_table.find_all('div', attrs={'class': 'currency'})
            for div_row in div_rows_list:
                div_td_list = div_row.find_all('div')
                currency_type = div_td_list[0].text.strip()

                # skip unsupported currencies
                if currency_type not in currency_type_mapper:
                    continue

                # convert original source currency type to our custom currency type
                currency_type = currency_type_mapper[currency_type]

                buy = to_decimal(div_td_list[1].text.strip())
                sale = to_decimal(div_td_list[2].text.strip())

                check_and_create_rate(base_currency_type, currency_type, source, sale, buy)
