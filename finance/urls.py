from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^accounts/$', views.accounts_list, 
        name='accounts_list'),    
    url(r'^accounts/add/$', views.add_account, 
        name='add_account'),
    url(r'^orders/add/$', views.add_order,
        name='add_order'),
    url(r'^orders/(?P<oid>\d+)/edit/$', views.edit_order,
        name='edit_order'),
    url(r'^orders/(?P<oid>\d+)/delete/$', views.delete_order,
        name='delete_order'),
]