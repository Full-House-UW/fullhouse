from datetime import (
    date, timedelta
)

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


from django.contrib.auth.decorators import login_required
from emailusernames.forms import EmailAuthenticationForm
from django.forms.formsets import formset_factory

from forms import *

from models import (
    House, Announcement, InviteProfile
)


def home(request):
    return HttpResponseRedirect('/welcome/')


@login_required
def create_announcement(request):
    # TODO Hack to block making an announcement if there's no house.
    if request.user.profile.house is None:
        return HttpResponseRedirect('/dashboard/')

    if request.method == "POST":
        announcement = Announcement(
            creator=request.user.profile,
            house=request.user.profile.house)
        form = CreateAnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        # Create a date two weeks from today.
        twoweeks = date.today() + timedelta(14)
        form = CreateAnnouncementForm(initial={'expiration': twoweeks})
    return render_to_response('create_announcement.html',
        RequestContext(request, {
            'form': form
        }))


@login_required
def edit_announcement(request):
    a = request.GET["id"] if request.method == "GET" else request.POST["id"]
    if a is None:
        #TODO decide how to handle this error.
        return HttpResponseRedirect('/dashboard/')
    try:
        announcement = Announcement.objects.get(id=a)
    except Announcement.DoesNotExist:
        # TODO decide how to handle this.
        return HttpResponseRedirect('/dashboard/')
    # Only the owner can edit.
    if request.user != announcement.creator.user:
        #TODO decide how to handle this.
        return HttpResponseRedirect('/dashboard/')

    if request.method == "POST":
        if request.POST.get('delete') is not None:
          announcement.delete()
          return HttpResponseRedirect('/dashboard/')
        form = CreateAnnouncementForm(request.POST, instance=announcement)
        if form.is_valid():
            announcement = form.save()
        return HttpResponseRedirect('/dashboard/')
    else:
        form = CreateAnnouncementForm(instance=announcement)
    return render_to_response('edit_announcement.html',
        RequestContext(request, {
            'form': form,
            'id': a
        }))


@login_required
def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = UpdateUserForm(request.POST, user=user)
        if form.is_valid():
            if form.cleaned_data['email'] != user.email:
                user.email = form.cleaned_data['email']
                user.save()
            user.profile.birthday = form.cleaned_data['birthday']
            user.profile.save()

            return HttpResponseRedirect('/dashboard/')
    else:
        initial = {
            'email': user.email,
            'birthday': user.profile.birthday,
        }
        form = UpdateUserForm(initial=initial, user=user)

    context = RequestContext(request, {'form': form})

    return render_to_response('user_settings.html', context)


@login_required
def edit_house(request):
    user = request.user
    house = user.profile.house
    if house is None:
        return HttpResponseRedirect('../create_house/')

    if request.method == "POST":
        form = CreateHouseForm(data=request.POST, instance=house)
        if form.is_valid():
            house.save()
            return HttpResponseRedirect('/dashboard/')

    else:
        initial = {
            'name': house.name,
            'zip_code': house.zip_code,
        }
        form = CreateHouseForm(initial=initial)
    context = RequestContext(request, {'form': form})

    return render_to_response('house_settings.html', context)


@login_required
def create_house(request):

    #TODO fix this hack
    user = request.user
    if user.profile.house is not None:
        form = CreateHouseForm(data=request.POST)
        context = RequestContext(request, {
            'error': 'You have already created a house',
        })
        return render_to_response('nonhousemember.html', context)

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
        else:
            context = RequestContext(request, {
                'form': form,
            })
            return render_to_response('nonhousemember.html', context)

        return HttpResponseRedirect('add_members/')

    else:
        form = CreateHouseForm()

    context = RequestContext(request, {
        'form': form,
    })
    return render_to_response('nonhousemember.html', context)


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

            return HttpResponseRedirect('/dashboard/')

    else:
        formset = AddMemberFormSet()

    context = RequestContext(request, {
        'formset': formset,
    })
    return render_to_response('addmembers/add_members.html', context)


@login_required
def dashboard(request):
# Make the user create/join a house before showing the dashboard.
    if request.user.profile.house is None:
        # TODO Don't see error for "already created house"
        return create_house(request)
        #return render_to_response('nonhousemember.html')
    else:
        return render_to_response('dashboard.html', {
            'announcements': request.user.profile.house.announcements.exclude(
                expiration__lt=date.today()
            )
        }, context_instance=RequestContext(request))


def welcome(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    form = EmailAuthenticationForm()
    return render_to_response('welcome.html',
        RequestContext(request, {
            'form': form
        }))


def about_us(request):
    return render_to_response('about_us.html')
