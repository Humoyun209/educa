from django.http import HttpResponse
from django.shortcuts import render
from django.apps import apps


def foo(request):
    print(apps.get_model(app_label='courses', model_name='course'))
    return HttpResponse('<h1>Hello, Educa</h1>')