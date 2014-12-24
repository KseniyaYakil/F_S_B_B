from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'session.views.home', name='home'),
    url(r'^verify/', 'session.views.verify_token', name='verify_token'),
)

