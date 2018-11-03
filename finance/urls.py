from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^accounts/$', views.accounts_list, 
        name='accounts_list'),    
    url(r'^accounts/add/$', views.add_account, 
        name='add_account'),
]