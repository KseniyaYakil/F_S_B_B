from django.conf.urls import patterns, include, url
from django.contrib import admin
from frontend import views

urlpatterns = patterns('',
		url(r'^$', 'frontend.views.home', name='home'),
		url(r'^login$', views.login, name='login'),
		url(r'^logout$', views.logout, name='logout'),
		url(r'^method/', views.method, name='method'),
		url(r'^position/create$', views.position_create, name='position_create'),
		url(r'^position/(?P<pos_id>\d+)$', views.position, name='position'),
		# url(r'^blog/', include('blog.urls')),
		url(r'^admin/', include(admin.site.urls)),
)
