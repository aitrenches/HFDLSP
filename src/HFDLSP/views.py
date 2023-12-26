from django.shortcuts import render
from django.http import HttpResponse


def answer(request):
    return HttpResponse("Hello, this is the index page.")
