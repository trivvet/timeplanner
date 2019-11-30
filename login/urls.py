from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login_auth, 
        name='form'),
    url(r'^logout/$', views.logout_auth, 
        name='out'),
    url(r'^attempts/$', views.login_attempts, 
        name='attempts'),
    url(r'^attempts/delete$', views.delete_old_attempts, 
        name='attempts_delete'),
]