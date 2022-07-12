from django.shortcuts import render

from django.http import HttpResponse


def hello_world(request):
    name = request.GET.get('name')
    result = ''
    if not request.GET.get('name'):
        result = 'Hello, World!'
    else:
        result = 'Hello, ' + name + '!'
    return HttpResponse(result)
