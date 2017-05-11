from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^getjobs$', views.getjobs, name='getjobs'),
    url(r'^jobs/$', views.jobs, name='jobs'),
    url(r'^log_in/$', views.log_in, name='log_in'),
    url(r'^log_out/$', views.log_out, name='log_out'),
    url(r'^sign_up/$', views.sign_up, name='sign_up'),
    url(r'^user_list/$', views.user_list, name='user_list'),
    url(r'^$', views.index, name='index'),
]