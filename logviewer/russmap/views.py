from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import os

def index(request):
    #print("===")
    #print(request)
    #print("====")
    if request.method == 'POST':
        for key, value in request.POST.items():
            print(key,value)

    load_file = open('static/'+request.path, mode='rb')
    if request.path == "/russ_map_panel.html":
        return HttpResponse(load_file, content_type='text/html')
