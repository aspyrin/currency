from django.shortcuts import render, redirect, get_object_or_404
from currency.models import Rate, ContactUs, Source
from currency.utils import rates_gen, contactus_gen
from currency.forms import RateForm, ContactUsForm, SourceForm


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


def source_list(request):
    """
    function return all records of Source model
    :param
    none
    :return:
    all records of Source model
    """
    context = {
        'title': 'Source list',
        'source_list': Source.objects.all(),
    }
    return render(request, 'source_list.html', context=context)


def source_create(request):
    """
    function create object of Source model
    :param
    none
    :return:
    redirect to /source_list/
    """
    if request.method == 'POST':
        form = SourceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/source_list/')
    elif request.method == 'GET':
        form = SourceForm()
    context = {
        'title': 'Source create',
        'form': form,
    }
    return render(request, 'source_create.html', context=context)


def source_update(request, source_id):
    """
    function update object of Source model by id
    :param
    none
    :return:
    redirect to /source_list/
    """
    source_instance = get_object_or_404(Source, id=source_id)

    if request.method == 'POST':
        form = SourceForm(request.POST, instance=source_instance)
        if form.is_valid():
            form.save()
            return redirect('/source_list/')
    elif request.method == 'GET':
        form = SourceForm(instance=source_instance)
    context = {
        'title': 'Source update',
        'form': form,
    }
    return render(request, 'source_update.html', context=context)


def source_details(request, source_id):
    """
    function return one object of Source model by id
    :param
    none
    :return:
    one object of Source model by id
    """
    source_instance = get_object_or_404(Source, id=source_id)
    context = {
        'title': 'Source details',
        'instance': source_instance,
    }
    return render(request, 'source_details.html', context=context)


def source_delete(request, source_id):
    """
    function delete object of Source model by id
    :param
    none
    :return:
    redirect to /source_list/
    """
    source_instance = get_object_or_404(Source, id=source_id)
    if request.method == 'POST':
        source_instance.delete()
        return redirect('/source_list/')
    context = {
        'title': 'Source delete',
        'instance': source_instance,
    }
    return render(request, 'source_delete.html', context=context)


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


def rate_create(request):
    """
    function create object of Rate model
    :param
    none
    :return:
    redirect to /rate_list/
    """
    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/rate_list/')
    elif request.method == 'GET':
        form = RateForm(initial={'base_currency_type': 'UAN'})
    context = {
        'title': 'Rate create',
        'form': form,
    }
    return render(request, 'rate_create.html', context=context)


def rate_update(request, rate_id):
    """
    function update object of Rate model by id
    :param
    none
    :return:
    redirect to /rate_list/
    """
    rate_instance = get_object_or_404(Rate, id=rate_id)

    if request.method == 'POST':
        form = RateForm(request.POST, instance=rate_instance)
        if form.is_valid():
            form.save()
            return redirect('/rate_list/')
    elif request.method == 'GET':
        form = RateForm(instance=rate_instance)
    context = {
        'title': 'Rate update',
        'form': form,
    }
    return render(request, 'rate_update.html', context=context)


def rate_details(request, rate_id):
    """
    function return one object of Rate model by id
    :param
    none
    :return:
    one object of Rate model by id
    """
    rate_instance = get_object_or_404(Rate, id=rate_id)
    context = {
        'title': 'Rate details',
        'instance': rate_instance,
    }
    return render(request, 'rate_details.html', context=context)


def rate_delete(request, rate_id):
    """
    function delete object of Rate model by id
    :param
    none
    :return:
    redirect to /rate_list/
    """
    rate_instance = get_object_or_404(Rate, id=rate_id)
    if request.method == 'POST':
        rate_instance.delete()
        return redirect('/rate_list/')
    context = {
        'title': 'Rate delete',
        'instance': rate_instance,
    }
    return render(request, 'rate_delete.html', context=context)


def contactus_generator(request):
    """
    function clear currency_contactus table,
    and insert records into currency_contactus table
    :param
    none
    :return:
    link to contactus_list
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


def contactus_create(request):
    """
    function create object of ContactUs model
    :param
    none
    :return:
    redirect to /contactus_list/
    """
    if request.method == 'POST':
        form = ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contactus_list/')
    elif request.method == 'GET':
        form = ContactUsForm(initial={'email_from': 'curency@gmail.com'})
    context = {
        'title': 'ContactUs create',
        'form': form,
    }
    return render(request, 'contactus_create.html', context=context)


def contactus_details(request, contactus_id):
    """
    function return one object of ContactUs model by id
    :param
    none
    :return:
    one object of ContactUs model by id
    """
    contactus_instance = get_object_or_404(ContactUs, id=contactus_id)
    context = {
        'title': 'ContactUs details',
        'instance': contactus_instance,
    }
    return render(request, 'contactus_details.html', context=context)


def contactus_delete(request, contactus_id):
    """
    function delete object of ContactUs model by id
    :param
    none
    :return:
    redirect to /contactus_list/
    """
    contactus_instance = get_object_or_404(ContactUs, id=contactus_id)
    if request.method == 'POST':
        contactus_instance.delete()
        return redirect('/contactus_list/')
    context = {
        'title': 'ContactUs delete',
        'instance': contactus_instance,
    }
    return render(request, 'contactus_delete.html', context=context)


def contactus_update(request, contactus_id):
    """
    function update object of ContactUs model by id
    :param
    none
    :return:
    redirect to /contactus_list/
    """
    contactus_instance = get_object_or_404(ContactUs, id=contactus_id)

    if request.method == 'POST':
        form = ContactUsForm(request.POST, instance=contactus_instance)
        if form.is_valid():
            form.save()
            return redirect('/contactus_list/')
    elif request.method == 'GET':
        form = ContactUsForm(instance=contactus_instance)
    context = {
        'title': 'ContactUs update',
        'form': form,
    }
    return render(request, 'contactus_update.html', context=context)
