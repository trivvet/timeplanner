from django.conf.urls import url

from . import views
from .views import (
    AccountDetail,
    OrderDetail,
    IncomeCreate, 
    IncomeEdit, 
    IncomeDelete,
    ExecutionCreate,
    ExecutionEdit,
    ExecutionDelete,
    )

urlpatterns = [
    # account URLs
    url(r'^accounts/$', views.accounts_list, 
        name='accounts_list'), 
    url(r'^account/(?P<pk>\d+)/detail/$', AccountDetail.as_view(),
        name='detail_account'),
    url(r'^accounts/add/$', views.add_account, 
        name='add_account'),
    url(r'^accounts/(?P<aid>\d+)/edit/$', views.edit_account,
        name='edit_account'),
    url(r'^accounts/(?P<aid>\d+)/delete/$', views.delete_account,
        name='delete_account'),

    # order URLs
    url(r'^orders/$', views.orders_list, 
        name='orders_list'),
    url(r'^orders/(?P<pk>\d+)/detail/$', OrderDetail.as_view(),
        name='detail_order'),   
    url(r'^orders/add/$', views.add_order,
        name='add_order'),
    url(r'^orders/(?P<oid>\d+)/edit/$', views.edit_order,
        name='edit_order'),
    url(r'^orders/(?P<oid>\d+)/delete/$', views.delete_order,
        name='delete_order'),

    # income URLs
    url(r'^incomes/$', views.incomes_list,
        name='incomes_list'),
    url(r'^incomes/add/$', IncomeCreate.as_view(),
        name="add_income"),
    url(r'^incomes/(?P<pk>\d+)/edit/$', IncomeEdit.as_view(),
        name="edit_income"),
    url(r'^incomes/(?P<pk>\d+)/delete/$', IncomeDelete.as_view(),
        name="delete_income"),

    # execution URLs
    url(r'^executions/$', views.executions_list,
        name='executions_list'),
    url(r'^executions/add/$', ExecutionCreate.as_view(),
        name="add_execution"),
    url(r'^executions/(?P<pk>\d+)/edit/$', ExecutionEdit.as_view(),
        name="edit_execution"),
    url(r'^executions/(?P<pk>\d+)/delete/$', ExecutionDelete.as_view(),
        name="delete_execution"),
]