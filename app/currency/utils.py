import random
from currency.models import Rate, ContactUs


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

    source = "privatbank"
    bc_type = "UAN"
    c_types = ["USD", "EUR", "GBP", "PLN", "FRF"]
    init_sale = {"USD": 36, "EUR": 37, "GBP": 39, "PLN": 6, "FRF": 5}

    Rate.objects.all().delete()

    for i in range(100):
        random.shuffle(c_types)
        cur_c_type = c_types[0]
        init_sale_value = init_sale.get(str(cur_c_type))
        cur_sale = init_sale_value + random.random()
        cur_buy = cur_sale * (1 + random.random())

        rate_object = Rate()
        rate_object.base_currency_type = bc_type
        rate_object.currency_type = cur_c_type
        rate_object.sale = cur_sale
        rate_object.buy = cur_buy
        rate_object.source = source
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
