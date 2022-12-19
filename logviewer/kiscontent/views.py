from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
import os

def index(request, loadfile):
    load_file = open('/home/rhandorf/kismet-logviewer/logviewer/static/'+request.path, mode='rb')
    if loadfile[-2:] == "js":
        return HttpResponse(load_file, content_type='application/javascript')
    elif loadfile[-3:] == "css":
        return HttpResponse(load_file, content_type='text/css')
    elif request.path[:6] == "/fonts":
        return HttpResponse(load_file, content_type='font/ttf')
    elif loadfile[:4] == "font":
        return HttpResponse(load_file, content_type='font/woff2')
    elif loadfile[:6] == "images":
        return HttpResponse(load_file, content_type='image/png')
    if request.path[0:11] == "/css/images":
        return HttpResponse(load_file, content_type='image/png')
    elif request.path[0:7] == "/images":
        return HttpResponse(load_file, content_type='image/png')
