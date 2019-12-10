from django.conf.urls import url

from django.contrib.auth.decorators import permission_required

from . import views
from .views import (
    AccountList,
    AccountDetail,
    OrderDetail,
    IncomeList,
    IncomeCreate, 
    IncomeEdit, 
    IncomeDelete,
    ExecutionList,
    ExecutionCreate,
    ExecutionEdit,
    ExecutionDelete,
    )

urlpatterns = [
    # account URLs
    url(r'^accounts/$', 
        permission_required('admins')(AccountList.as_view()), 
        name='accounts_list'), 
    url(r'^account/(?P<pk>\d+)/detail/$', 
        permission_required('admins')(AccountDetail.as_view()),
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
    url(r'^orders/(?P<pk>\d+)/detail/$', 
        permission_required('admins')(OrderDetail.as_view()),
        name='detail_order'),   
    url(r'^orders/add/$', views.add_order,
        name='add_order'),
    url(r'^orders/(?P<oid>\d+)/edit/$', views.edit_order,
        name='edit_order'),
    url(r'^orders/(?P<oid>\d+)/delete/$', views.delete_order,
        name='delete_order'),

    # income URLs
    url(r'^incomes/$', 
        permission_required('admins')(IncomeList.as_view()), 
        name="incomes_list"),
    url(r'^incomes/add/$', 
        permission_required('admins')(IncomeCreate.as_view()),
        name="add_income"),
    url(r'^incomes/(?P<pk>\d+)/edit/$', 
        permission_required('admins')(IncomeEdit.as_view()),
        name="edit_income"),
    url(r'^incomes/(?P<pk>\d+)/delete/$', 
        permission_required('admins')(IncomeDelete.as_view()),
        name="delete_income"),

    # execution URLs
    url(r'^executions/$', 
        permission_required('admins')(ExecutionList.as_view()), 
        name='executions_list'),
    url(r'^executions/add/$', 
        permission_required('admins')(ExecutionCreate.as_view()),
        name="add_execution"),
    url(r'^executions/(?P<pk>\d+)/edit/$', 
        permission_required('admins')(ExecutionEdit.as_view()),
        name="edit_execution"),
    url(r'^executions/(?P<pk>\d+)/delete/$', 
        permission_required('admins')(ExecutionDelete.as_view()),
        name="delete_execution"),
]