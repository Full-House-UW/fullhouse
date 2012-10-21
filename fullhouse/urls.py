from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('fullhouse.dashboard',
    # Examples:
    url(r'^$', 'views.welcome', name='welcome'),
    url(r'^login/$', 'views.login', name='login'),
    url(r'^dashboard/$', 'views.dashboard', name='dashboard'),

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
