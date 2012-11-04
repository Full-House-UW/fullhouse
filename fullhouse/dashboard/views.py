from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.forms.formsets import formset_factory

from forms import (
    CreateHouseForm, AddMemberForm, BaseAddMemberFormSet
)
from models import (
    House, InviteProfile
)


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

        return HttpResponseRedirect('../add_members/')

    else:
        form = CreateHouseForm()

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response('create_house.html', context)


@login_required
def join_house(request, invite_key):
    user = request.user
    joined = InviteProfile.objects.accept_invite(user, invite_key)
        # redirect to success url
    context = RequestContext(request, {
        'joined': joined,
    })

    return render_to_response('addmembers/__accept.html', context)


@login_required
def add_members(request):
    user = request.user
    if user.profile.house is None:
        return HttpResponseRedirect('../create_house')

    AddMemberFormSet = formset_factory(
        AddMemberForm,
        extra=3,
        max_num=12,
        formset=BaseAddMemberFormSet
    )
    if request.method == "POST":
        formset = AddMemberFormSet(data=request.POST)
        if formset.is_valid():
            # do something with data
            # pdb.set_trace()
            for f in formset.cleaned_data:
                if 'email' in f:
                    email = f['email']
                    InviteProfile.objects.create_member_invite(
                        email, user, user.profile.house
                    )

            return HttpResponseRedirect('complete/')

    else:
        formset = AddMemberFormSet()

    context = RequestContext(request, {
        'formset': formset,
    })
    return render_to_response('addmembers/add_members.html', context)


@login_required
def dashboard(request):
    return render_to_response('dashboard.html')


def welcome(request):
    form = AuthenticationForm()
    return render_to_response('welcome.html',
        RequestContext(request, {
            'form': form
        }))
