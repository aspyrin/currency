# from django.shortcuts import render

from django.http import HttpResponse
from currency.models import Rate, ContactUs
from currency.utils import rates_gen, contactus_gen


def rate_generator(request):
    """
    function clear currency_rate table,
    generate random values and insert 100 records into currency_rate table
    :param
    none
    :return:
    link to rate_list
    """
    rates_gen()
    result = '''Выполнена генерация и добавление в модель Rate 100 записей<br>
                <a href="/rate_list/">Перейти к списку >>></a>'''
    return HttpResponse(result)


def rate_list(request):
    """
    function return all records of Rate model
    :param
    none
    :return:
    all records of Rate model
    """
    rates_list = []
    for rate in Rate.objects.all():
        html_string = f'''ID: {rate.id},
                            bc_type: '{rate.base_currency_type}',
                            c_type: '{rate.currency_type}',
                            sale: {rate.sale},
                            buy: {rate.buy},
                            source: '{rate.source}',
                            created: '{rate.created.strftime("%x %X")}'<br>'''
        html_string = html_string.replace("\n ", "")
        rates_list.append(html_string)
    return HttpResponse(str(rates_list))


def contactus_generator(request):
    """
    function clear currency_contactus table,
    and insert records into currency_contactus table
    :param
    none
    :return:
    link to rate_list
    """
    contactus_gen()
    result = '''Выполнена генерация и добавление в модель ContactUs 100 записей <br>
                <a href="/contactus_list/">Перейти к списку >>></a>'''
    return HttpResponse(result)


def contactus_list(request):
    """
    function show all records of model ContactUs
    :param
    no
    :return:
    all records of model ContactUs
    """
    contactus_list = []
    for contactus in ContactUs.objects.all():
        html_string = f'''ID: {contactus.id},
                            email_from: '{contactus.email_from}',
                            email_to: '{contactus.email_to}',
                            subject: '{contactus.subject}',
                            message: ({contactus.message}),
                            sended: '{contactus.sended.strftime("%x %X")}'<br>'''
        html_string = html_string.replace("\n ", "")
        contactus_list.append(html_string)
    return HttpResponse(str(contactus_list))
