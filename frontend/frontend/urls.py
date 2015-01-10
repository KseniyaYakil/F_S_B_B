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
		url(r'^position/(?P<pos_id>\d+)/delete$', views.position_delete, name='position_delete'),
		url(r'^position/(?P<pos_id>\d+)/modify$', views.position_modify, name='position_modify'),
		url(r'^position/all$', views.position_all, name='position_all'),

		url(r'^employe/create$', views.employe_create, name='employe_create'),
		url(r'^employe/(?P<emp_id>\d+)$', views.employe, name='employe'),
		url(r'^employe/(?P<emp_id>\d+)/delete$', views.employe_delete, name='employe_delete'),
		url(r'^employe/(?P<emp_id>\d+)/modify$', views.employe_modify, name='employe_modify'),
		url(r'^admin/', include(admin.site.urls)),
)
