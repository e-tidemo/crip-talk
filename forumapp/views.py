from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def crip_talk(request):
    return HttpResponse("Hello, forum!")