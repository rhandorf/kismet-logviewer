from django.shortcuts import render, redirect

from django.http import HttpResponse, HttpRequest

# Create your views here.

def eventbus(request):
    #print("=============")
    #print(request)
    return HttpResponse(request, content_type='text/json')

def index(request):
    #print("=============")
    #print(request)
    #print(event_name)
    #print("-------------")
    return HttpResponse("[]", content_type='text/json')
