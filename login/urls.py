from django.conf.urls import url

from axes.decorators import watch_login

from . import views

urlpatterns = [
    url(r'^login/$', watch_login(views.login_auth), 
        name='login_form'),
    url(r'^logout/$', views.logout_auth, 
        name='logout_url'),
    url(r'^login/attempts/$', views.login_attempts, 
        name='login_attempts'),
]