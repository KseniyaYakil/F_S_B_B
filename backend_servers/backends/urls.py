from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'backends.views.home', name='home'),
    url(r'^positions/', 'backends.views.positions', name='positions'),
    url(r'^position/(?P<pos_id>\d+)$', 'backends.views.position', name='position'),

    url(r'^employes/', 'backends.views.employes', name='employes'),
)

