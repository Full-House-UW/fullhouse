from django.conf.urls import patterns, include, url
from django.views.generic.simple import direct_to_template

import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^create_house/$',
        views.create_house,
        name='dashboard_create_house'),
    url(r'^add_members/$',
        views.add_members,
        name='dashboard_add_members'),
    url(r'^add_members/complete/$',
        direct_to_template,
        {'template': 'addmembers/add_members_complete.html'}),
    url(r'^join_house/(?P<invite_key>\w+)/$',
        views.join_house,
        name='dashboard_join_house'),
    url(r'^announcement/new/$',
        views.create_announcement,
        name='create_announcement'),
    url(r'^announcement/edit/$',
        views.edit_announcement,
        name='edit_announcement'),
    url(r'^user_settings/$',
        views.edit_user,
        name='edit_user'),
    url(r'^house_settings/$',
        views.edit_house,
        name='edit_house'),
)
