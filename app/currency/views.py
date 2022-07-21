from django.shortcuts import render, redirect
from currency.models import Rate, ContactUs
from currency.utils import rates_gen, contactus_gen


def index(request):
    """
    :param
    none
    :return:
    link to home page
    """
    context = {
        'title': 'Home page',
        'message': 'Currency exchange project',
    }
    return render(request, 'index.html', context=context)


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
    return redirect('/rate_list/')


def rate_list(request):
    """
    function return all records of Rate model
    :param
    none
    :return:
    all records of Rate model
    """
    context = {
        'title': 'Rate list',
        'rate_list': Rate.objects.all(),
    }
    return render(request, 'rate_list.html', context=context)


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
    return redirect('/contactus_list/')


def contactus_list(request):
    """
    function show all records of model ContactUs
    :param
    no
    :return:
    all records of model ContactUs
    """
    context = {
        'title': 'Contact Us list',
        'contactus_list': ContactUs.objects.all(),
    }
    return render(request, 'contactus_list.html', context=context)
