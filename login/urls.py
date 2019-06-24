from django.conf.urls import url

from axes.decorators import watch_login

from . import views

urlpatterns = [
    url(r'^$', watch_login(views.login_auth), 
        name='form'),
    url(r'^logout/$', views.logout_auth, 
        name='out'),
    url(r'^attempts/$', views.login_attempts, 
        name='attempts'),
    url(r'^attempts/delete$', views.delete_old_attempts, 
        name='attempts_delete'),
]