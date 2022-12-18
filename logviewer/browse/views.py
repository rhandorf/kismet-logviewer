from django.shortcuts import render
from django.http import HttpResponse

load_db=0
display_data=1

context = {
  'load_db': load_db,
  'display_data': display_data,
}

def index(request):
    #if load_db == 0:
    #  return HttpResponse("Gotta load a DB")
    #else:
    #  return HttpResponse("DB loaded")

    return render(request, 'index.html', context=context)
