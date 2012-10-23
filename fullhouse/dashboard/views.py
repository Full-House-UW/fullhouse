from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return HttpResponseRedirect('/welcome/')


def welcome(request):
    form = AuthenticationForm()
    return render_to_response('welcome.html',
        RequestContext(request, {
            'form': form
        }))


@login_required(login_url='/accounts/login/')
def dashboard(request):
    return render_to_response('dashboard.html')

