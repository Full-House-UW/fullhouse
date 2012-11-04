from django.conf.urls import patterns, include, url

import views

urlpatterns = patterns('',
    url(r'^$', views.dashboard, name='dashboard'),
    url(r'^create_house/$',
        views.create_house,
        name='dashboard_create_house'),
    url(r'^create_house/complete/$',
        views.create_house,
        {'template_name': 'create_house_complete'},
        name='dashboard_create_house_complete'),
    url(r'^announcement/new/$',
        views.create_announcement,
        name='create_announcement'),
)
