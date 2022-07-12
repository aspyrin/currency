# from django.shortcuts import render

from django.http import HttpResponse


def hello_world(request):
    """
    Test function
    :param
    request: name
    :return:
    if no get param -> Hello, World!
    if get param 'name' -> Hello, <Name>!
    """

    name = request.GET.get('name')
    if not request.GET.get('name'):
        result = 'Hello, World!'
    else:
        result = 'Hello, ' + name + '!'
    return HttpResponse(result)
