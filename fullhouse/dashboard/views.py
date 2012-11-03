from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm

from forms import CreateHouseForm
from models import House


def home(request):
    return HttpResponseRedirect('/welcome/')


@login_required
def create_house(request):

    #TODO fix this hack
    user = request.user
    if user.profile.house is not None:
        form = CreateHouseForm(data=request.POST)
        context = RequestContext(request, {
            'error': 'You have already created a house',
        })
        return render_to_response('create_house.html', context)

    if request.method == "POST":
        # create the house and redirect to complete page
        form = CreateHouseForm(data=request.POST)
        if form.is_valid():
            userprofile = request.user.profile
            name = form.cleaned_data['name']
            zip_code = form.cleaned_data['zip_code']
            new_house = House.objects.create(name=name, zip_code=zip_code)
            new_house.save()
            userprofile.house = new_house
            userprofile.save()

        return HttpResponseRedirect('complete/')

    else:
        form = CreateHouseForm()

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response('create_house.html', context)


@login_required
def dashboard(request):
    return render_to_response('dashboard.html')


def welcome(request):
    form = AuthenticationForm()
    return render_to_response('welcome.html',
        RequestContext(request, {
            'form': form
        }))
