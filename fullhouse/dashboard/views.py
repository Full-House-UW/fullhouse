from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


def home(request):
    return HttpResponseRedirect('/welcome/')


def welcome(request):
    return render_to_response('welcome.html',
        RequestContext(request, {}))


def login(request):
    return HttpResponseRedirect('/dashboard/')


def logout(request):
    return HttpResponseRedirect('/')


def dashboard(request):
    return render_to_response('dashboard.html')
    
def registration(request):
    return render_to_response('registration.html')
