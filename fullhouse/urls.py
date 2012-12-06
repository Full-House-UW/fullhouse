from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from fullhouse.dashboard import views

urlpatterns = patterns(
    '',
    url(r'^$', views.home, name='home'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^about_us/$', views.about_us, name='about_us'),
    url(r'^dashboard/', include('fullhouse.dashboard.urls')),
    url(r'^accounts/', include('fullhouse.auth.urls')),
    url(r'^faq/$', views.faq, name='faq'),
    url(r'^contact_us/$', views.contact_us, name='contact_us'),
    url(r'^handler403/$', views.handler403, name='handler403'),
    url(r'^handler404/$', views.handler404, name='handler404'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


# for debug only! django is not made to serve static files in prod
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
