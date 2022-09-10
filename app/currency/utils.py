import random
from currency.models import Rate, ContactUs, Source
import datetime
from decimal import Decimal


def rates_gen():
    """
    function clear currency_rate table and insert 100 records into currency_rate table
    rate.currency_type - determined randomly from the list
    rate. sale - determined randomly based on the initial values for each type of currency
    rate. buy - calculated by the formula
    :param clear: if true -> delete oll objects before insert
    :param num: number of objects to add
    :return: none
    """

    bc_type = "UAH"
    c_types = ["USD", "EUR", "BTC"]
    # sources = ["privatbank", "monobank"]
    sources = Source.objects.all()
    init_sale = {"USD": 36, "EUR": 37, "BTC": 863932}

    date_list = []
    for i in range(10):
        create_date = datetime.datetime.date(datetime.datetime.now() + datetime.timedelta(days=-i))
        date_list.append(create_date)

    Rate.objects.all().delete()

    for date in date_list:
        for c_type in c_types:
            for source in sources:
                cur_c_type = c_type
                init_sale_value = init_sale.get(str(cur_c_type))
                cur_sale = init_sale_value + random.random()
                cur_buy = cur_sale - random.random()

                rate_object = Rate()
                rate_object.base_currency_type = bc_type
                rate_object.currency_type = cur_c_type
                rate_object.sale = cur_sale
                rate_object.buy = cur_buy
                rate_object.source = source
                rate_object.save()
                rate_object.created = date
                rate_object.save()


def contactus_gen():
    emails_list = ["receiver1@gmail.com",
                   "rreceiver2@gmail.com",
                   "receiver3@gmail.com",
                   "receiver4@gmail.com",
                   "receiver5@gmail.com"]

    ContactUs.objects.all().delete()

    for rate in Rate.objects.all():
        random.shuffle(emails_list)
        subject = f'Current exchange rate on date {rate.created.strftime("%x %X")}'
        message = f'''base_currency_type: {rate.base_currency_type},
                        currency_type: {rate.currency_type},
                        sale: {str(rate.sale)},
                        buy: {str(rate.buy)},
                        source: {rate.source}'''

        ContactUs.objects.create(email_from='curency@gmail.com',
                                 email_to=emails_list[0],
                                 subject=subject,
                                 message=message)


def get_last_rate_date():
    if Rate.objects.all().count() > 0:
        try:
            last_rate_date = Rate.objects.last().created
            return last_rate_date
        except Rate.DoesNotExist:
            return None
    else:
        return None


def get_last_rate_list(sort_params: str = 'sale_asc') -> list:
    unique_rows = Rate.objects.values('base_currency_type', 'currency_type', 'source_id').distinct()
    last_rate_list = list()
    for row in unique_rows:
        try:
            last_rate = Rate.objects.select_related('source').filter(
                base_currency_type=row['base_currency_type'],
                currency_type=row['currency_type'],
                source_id=row['source_id'],
            ).latest('created')
            last_rate_list.append(last_rate)
        except Rate.DoesNotExist:
            last_rate = None

    # sort final object list
    if sort_params == 'sale_asc':
        last_rate_list.sort(key=lambda x: x.sale, reverse=False)
    elif sort_params == 'sale_desc':
        last_rate_list.sort(key=lambda x: x.sale, reverse=True)
    elif sort_params == 'buy_asc':
        last_rate_list.sort(key=lambda x: x.buy, reverse=False)
    elif sort_params == 'buy_desc':
        last_rate_list.sort(key=lambda x: x.buy, reverse=True)

    return last_rate_list


def get_currency_types():
    if Rate.objects.all().count() > 0:
        try:
            currency_type_list = Rate.objects.values('base_currency_type', 'currency_type').distinct()
            return currency_type_list
        except Rate.DoesNotExist:
            return None
    else:
        None


def to_decimal(value: str, precision: int = 4) -> Decimal:
    """
    :param value:
    :param precision:
    :return: raunded decimal result
    """
    return Decimal(round(Decimal(value), 4))


def check_and_create_rate(base_currency_type: str,
                          currency_type: str,
                          source: Source,
                          sale: Decimal,
                          buy: Decimal):
    """

    :param base_currency_type:
    :param currency_type:
    :param source:
    :param sale:
    :param buy:
    :return:
    """
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
