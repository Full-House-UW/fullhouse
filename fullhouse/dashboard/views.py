from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

def welcome(request):
    return render_to_response('welcome.html',
        RequestContext(request, {}))

def login(request):
    return HttpResponseRedirect('/dashboard/')

def dashboard(request):
    return render_to_response('dashboard.html')
