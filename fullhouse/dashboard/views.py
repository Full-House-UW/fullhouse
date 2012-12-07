from datetime import (
    date, timedelta
)
import pdb

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext


from django.contrib.auth.decorators import login_required
from emailusernames.forms import EmailAuthenticationForm
from django.forms.models import model_to_dict
from django.forms.formsets import formset_factory

from forms import *

from models import *


def get_param(request, key):
    if request.method == "GET":
        return request.GET.get(key, None)
    else:
        return request.POST.get(key, None)


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

    return render_to_response(
        'create_announcement.html',
        RequestContext(request, {
            'form': form,
            'error': get_param(request, 'error'),
            'message': get_param(request, 'message'),
            'time': get_param(request, 'time')
        })
    )


@login_required
def edit_announcement(request):
    #TODO fix this, will break if id not passed in
    a = request.GET["id"] if request.method == "GET" else request.POST["id"]
    if a is None:
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
    return render_to_response(
        'edit_announcement.html',
        RequestContext(request, {
            'form': form,
            'id': a,
            'error': get_param(request, 'error'),
            'message': get_param(request, 'message'),
            'time': get_param(request, 'time')
        }))


@login_required
def create_task(request):
    userprofile = request.user.profile
    if userprofile.house is None:
        return HttpResponseRedirect('/dashboard/')
    members = userprofile.house.members.get_query_set()

    if request.method == "POST":
        form = CreateTaskForm(request.POST, members=members)
        if form.is_valid():
            Task.objects.create_task(userprofile, form)
            return HttpResponseRedirect('/dashboard/')
    else:
        form = CreateTaskForm(members=members)
    return render_to_response(
        'create_task.html',
        RequestContext(request, {
            'form': form,
            'error': get_param(request, 'error'),
            'message': get_param(request, 'message'),
            'time': get_param(request, 'time')
        }))


@login_required
def edit_task(request):
    t_id = None
    if request.method == "GET":
        t_id = request.GET.get('id', None)
    elif request.method == "POST":
        t_id = request.POST.get('id', None)
    if t_id is None:
        return HttpResponseRedirect('/dashboard/')

    try:
        task = Task.objects.get(id=t_id)
    except Task.DoesNotExist:
        # TODO decide how to handle this.
        return HttpResponseRedirect('/dashboard/')

    userprofile = request.user.profile
    members = userprofile.house.members.get_query_set()

    # Only the members of this task's house can edit.
    if userprofile not in task.house.members.all():
        #TODO decide how to handle this.
        return HttpResponseRedirect('/dashboard/')

    if request.method == "POST":
        #TODO use discontinue instead of delete
        if request.POST.get('discontinue') is not None:
            task.is_active = False
            task.save()
            return HttpResponseRedirect('/dashboard/')
        form = CreateTaskForm(request.POST, instance=task, members=members)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/dashboard/')
    else:
        form = CreateTaskForm(instance=task, members=members)
    return render_to_response(
        'edit_task.html',
        RequestContext(request, {
            'form': form,
            'id': t_id,
            'error': get_param(request, 'error'),
            'message': get_param(request, 'message'),
            'time': get_param(request, 'time')
        }))


@login_required
def update_task(request, action):
    redirect = request.GET.get('next', '/dashboard/')

    t_id = request.GET.get("id", None)
    if t_id is not None:
        userprofile = request.user.profile
        Task.objects.update_taskinstance(t_id, userprofile, action)
    return HttpResponseRedirect(redirect)


@login_required
def task_history(request):
    if request.user.profile.house is None:
        return HttpResponseRedirect('/dashboard/')

    house = request.user.profile.house
    taskhistory = Task.objects.get_task_history(house)
    context = RequestContext(request, {'tasks': taskhistory})

    return render_to_response('task_history.html', context)


@login_required
def edit_user(request):
    user = request.user
    if request.method == "POST":
        form = UpdateUserForm(request.POST, instance=user.profile)
        if form.is_valid():
            form.save()

            return HttpResponseRedirect('/dashboard/')
    else:
        initial = model_to_dict(user.profile)
        initial['first_name'] = user.first_name
        initial['last_name'] = user.last_name
        form = UpdateUserForm(initial=initial)

    context = RequestContext(request, {
        'form': form,
        'error': get_param(request, 'error'),
        'message': get_param(request, 'message'),
        'time': get_param(request, 'time')
    })

    return render_to_response('user_settings.html', context)


@login_required
def edit_house(request):
    user = request.user
    house = user.profile.house
    if house is None:
        return HttpResponseRedirect('/dashboard/')

    AddMemberFormSet = formset_factory(
        AddMemberForm,
        extra=3
    )

    # default values to be passed to templates -- changed below on certain
    # condition
    initial = {
        'name': house.name,
        'zip_code': house.zip_code,
    }
    form = CreateHouseForm(initial=initial)
    formset = AddMemberFormSet()
    message = get_param(request, 'message')
    time = get_param(request, 'time')

    if request.method == "POST":
        form = CreateHouseForm(data=request.POST, instance=house)
        formset = AddMemberFormSet(data=request.POST)

        # leaving the house is a separate command and does not
        # touch form data
        if request.POST.get('leave_house') is not None:
            user.profile.house = None
            user.profile.save()
            return HttpResponseRedirect('/dashboard/')

        if formset.is_valid() and form.is_valid():
            form.save()  # Update the house

            # process the invitations:
            current_member_emails = [member.user.email for member in house.members.all()]
            current_invitee_emails = [invitee.email for invitee in house.invitees.all() if not invitee.invite_key_expired()]
            emails_not_invited = []
            for f in formset.cleaned_data:
                if 'email' in f:
                    email = f['email']
                    if email in current_member_emails or email in current_invitee_emails:
                        emails_not_invited.append(email)
                    else:
                        InviteProfile.objects.create_member_invite(
                            email, user, user.profile.house
                        )
            # process house removal
            if form.cleaned_data['remove_from_house']:
                user.profile.house = None
                user.profile.save()

            # reset the add member formset so that the email they just entered
            # isn't displayed again
            formset = AddMemberFormSet()
            message = "House settings have been saved"
            time = "3"
            if len(emails_not_invited) != 0:
                message += ", but the following members were not invited " + \
                    "because they are already part of the house, or they have " + \
                    "already been invited: " + ', '.join(emails_not_invited)
                # since we have such a long message, don't fade it out
                time = None

    # process canceling of invitations
    elif request.method == "GET":
        uninvite_email = request.GET.get('uninvite', None)
        # it should never happen that there is more than one for a single
        # email, but just to be safe, let's deal with that case
        invites = house.invitees.filter(email=uninvite_email)
        for invite in invites:
            invite.delete()
        # deliberately continue without returning so we stay on this page

    members = [unicode(member) for member in house.members.all()]
    all_invitees = house.invitees.all()
    invitees = [x.email for x in all_invitees if not x.invite_key_expired()]
    if house.members.count() == 1:
            leave_message = "WARNING: you are the only member of %s. \
                             If you leave the house it will be deleted. \
                             Are you sure you want to leave?" % house.name
    else:
            leave_message = "If you leave %s, you will need an invitation \
                             from a house member to join again. Are you sure \
                             you want to leave?" % house.name

    context = RequestContext(request, {
        'form': form,
        'formset': formset,
        'members': members,
        'invitees': invitees,
        'leave_message': leave_message,
        'error': get_param(request, 'error'),
        'message': message,
        'time': time,
    })

    return render_to_response('house_settings.html', context)


@login_required
def create_house(request):
    #TODO fix this hack
    user = request.user
    if user.profile.house is not None:
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

            return HttpResponseRedirect('add_members/')

    else:
        form = CreateHouseForm()

    context = RequestContext(request, {
        'form': form,
        'error': get_param(request, 'error'),
        'message': get_param(request, 'message'),
        'time': get_param(request, 'time')
    })

    return render_to_response('nonhousemember.html', context)


@login_required
def join_house(request, invite_key):
    user = request.user
    joined = InviteProfile.objects.accept_invite(user, invite_key)
        # redirect to success url
    context = RequestContext(request, {
        'joined': joined,
        'error': get_param(request, 'error'),
        'message': get_param(request, 'message'),
        'time': get_param(request, 'time')
    })

    return render_to_response('addmembers/__accept.html', context)


@login_required
def add_members(request):
    user = request.user
    if user.profile.house is None:
        return HttpResponseRedirect('/dashboard/')

    AddMemberFormSet = formset_factory(
        AddMemberForm,
        extra=3,
        formset=BaseAddMemberFormSet
    )
    if request.method == "POST":
        formset = AddMemberFormSet(data=request.POST)
        if formset.is_valid():
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
        'error': get_param(request, 'error'),
        'message': get_param(request, 'message'),
        'time': get_param(request, 'time')
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
        house = request.user.profile.house
        announcements = house.announcements.exclude(
            expiration__lt=date.today()
        )
        #pdb.set_trace()
        tasks = Task.objects.get_house_task_list(house)
        context = RequestContext(request, {
            'announcements': announcements,
            'tasks': tasks,
            'error': get_param(request, 'error'),
            'message': get_param(request, 'message'),
            'time': get_param(request, 'time')
        })
        return render_to_response('dashboard.html', context)


def welcome(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    form = EmailAuthenticationForm()
    return render_to_response(
        'welcome.html',
        RequestContext(request, {
            'form': form,
            'error': get_param(request, 'error'),
            'message': get_param(request, 'message'),
            'time': get_param(request, 'time')
        }))


def about_us(request):
    return render_to_response('about_us.html', RequestContext(request, {
        'error': get_param(request, 'error'),
        'message': get_param(request, 'message'),
        'time': get_param(request, 'time')
    }))


def faq(request):
    return render_to_response('faq.html', RequestContext(request, {
        'error': get_param(request, 'error'),
        'message': get_param(request, 'message'),
        'time': get_param(request, 'time')
    }))


def contact_us(request):
    return render_to_response('contact_us.html', RequestContext(request, {
        'error': get_param(request, 'error'),
        'message': get_param(request, 'message'),
        'time': get_param(request, 'time')
    }))
