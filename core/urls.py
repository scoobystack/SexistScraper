from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^jobs/$', views.jobs, name='jobs'),
    url(r'^getjobs$', views.getjobs, name='getjobs')
]