from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from fullhouse.dashboard import views
print views

urlpatterns = patterns('',
    # Examples:
    url(r'^$', views.home, name='home'),
    url(r'^welcome/$', views.welcome, name='welcome'),
    url(r'^about_us/', views.about_us, name='about_us'),
    url(r'^dashboard/', include('fullhouse.dashboard.urls')),
    url(r'^accounts/', include('fullhouse.auth.backend.urls')),


    # url(r'^fullhouse/', include('fullhouse.foo.urls')),

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
