from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'backend_servers.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
		url(r'^session/', include('session.urls')),
		url(r'^backends/', include('backends.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
