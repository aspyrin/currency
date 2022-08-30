from celery import shared_task
import requests
from settings import settings
from django.core.mail import send_mail
from time import sleep

from currency.utils import to_decimal
from currency import consts
from currency import model_choices as mch


@shared_task
def slow_func():
    print('START')
    sleep(3)
    print('END')


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
    from currency.models import Source, Rate

    source_name = 'PrivatBank'
    url = 'https://api.privatbank.ua/p24api/pubinfo?exchange&json&coursid=11'
    currency_type_mapper = {
        'UAH': mch.CarrencyType.CURRENCY_TYPE_UAH,
        'USD': mch.CarrencyType.CURRENCY_TYPE_USD,
        'EUR': mch.CarrencyType.CURRENCY_TYPE_EUR,
        'BTC': mch.CarrencyType.CURRENCY_TYPE_BTC,
    }

    response = requests.get(url)
    response.raise_for_status()  # raise error if not OK
    response_data = response.json()

    # get_or_create (if source object is not exist -> create it)
    # if created == True object was created, if created == False object was get from db
    source, created = Source.objects.get_or_create(code_name=consts.CODE_NAME_PRIVATBANK,
                                                   defaults={
                                                       'source_url': url,
                                                       'name': source_name,
                                                   })

    for rate_data in response_data:
        currency_type = rate_data['ccy']
        base_currency_type = rate_data['base_ccy']

        # skip unsupported currencies
        if currency_type not in currency_type_mapper or base_currency_type not in currency_type_mapper:
            continue

        # convert original source currency type to our custom currency type
        currency_type = currency_type_mapper[rate_data['ccy']]
        base_currency_type = currency_type_mapper[rate_data['base_ccy']]

        buy = to_decimal(rate_data['buy'])
        sale = to_decimal(rate_data['sale'])

        try:
            latest_rate = Rate.objects.filter(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                source=source,
            ).latest('created')
        except Rate.DoesNotExist:
            latest_rate = None

        if latest_rate is None or \
                latest_rate.sale != sale or \
                latest_rate.buy != buy:
            Rate.objects.create(
                base_currency_type=base_currency_type,
                currency_type=currency_type,
                sale=sale,
                buy=buy,
                source=source,
            )
