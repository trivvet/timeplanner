# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView
    )
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from ..models import Income, Order, Account
from ..forms import IncomeForm
from . import order_auto_create

@login_required(login_url='/login/')
def incomes_list(request):
    incomes = Income.objects.all()
    return render(request, 'finance/incomes_list.html', 
        {'incomes': incomes})

@method_decorator(login_required, name='dispatch')
class IncomeCreate(SuccessMessageMixin, CreateView):
    template_name = 'finance/form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('finance:incomes_list')

    def get_context_data(self, **kwargs):
        context = super(IncomeCreate, self).get_context_data(**kwargs)
        context['header'] = u"Додавання надходження"
        form = context['form']
        form.fields['order'].queryset = Order.objects.filter(
            status='inactive')
        return context

    def render_to_response(self, context):
        if self.request.GET.get('format') == 'json':
            order_id = self.request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
            must_pay = order.total_sum - order.paid_sum
            return JsonResponse(
                {'total_sum': must_pay}
            )
        else:
            return super(IncomeCreate, self).render_to_response(context)

    def form_valid(self, form):
        data = form.cleaned_data
        money = int(data['amount'])
        order = data['order']
        account = data['account']
        order.status = 'active'
        order.paid_sum += money
        order.save()
        account.total_sum += money
        account.save()
        return super(IncomeCreate, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        income = self.object
        message = u"{} успішно додане!".format(
            income)
        return message

@method_decorator(login_required, name='dispatch')
class IncomeEdit(SuccessMessageMixin, UpdateView):
    model = Income
    template_name = 'finance/form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('finance:incomes_list')

    def get_context_data(self, **kwargs):
        context = super(IncomeEdit, self).get_context_data(**kwargs)
        context['header'] = u"Редагування надходження"
        form = context['form']
        form.fields['order'].queryset = Order.objects.filter(
            status='active')
        form.fields['order'].widget.attrs['disabled'] = 'disabled'
        
        return context

    def render_to_response(self, context):
        if self.request.GET.get('format') == 'json':
            order_id = self.request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
            return JsonResponse(
                {'total_sum': order.total_sum}
            )
        else:
            return super(IncomeEdit, self).render_to_response(context)
    
    def post(self, request, *args, **kwargs):
        # import pdb;pdb.set_trace()
        income_id = kwargs['pk']
        income = Income.objects.get(pk=income_id)
        order_id = income.order.id
        request.POST = request.POST.copy()
        request.POST['order'] = order_id
        return super(IncomeEdit, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        initial_data = form.initial
        account_id = initial_data['account']
        account = Account.objects.get(pk=account_id)
        if data['amount'] != initial_data['amount']:
            difference_sum = data['amount'] - initial_data['amount']
            account.total_sum += difference_sum
            data['order'].paid_sum += difference_sum
            account.save()
            data['order'].save()
        if data['account'] != account:
            account.total_sum -= data['amount']
            account.save()
            new_account = data['account']
            new_account.total_sum += data['amount']
            new_account.save()
        return super(IncomeEdit, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        income = self.object
        message = u"{} успішно змінене!".format(
            income)
        return message

@method_decorator(login_required, name='dispatch')
class IncomeDelete(DeleteView):
    model = Income
    template_name = 'finance/confirm_delete.html'
    success_url = reverse_lazy('finance:incomes_list')

    def get_context_data(self, **kwargs):
        context = super(IncomeDelete, self).get_context_data(**kwargs)
        context['header'] = u"Видалення надходження"
        return context

    def delete(self, request, *args, **kwargs):
        income = self.get_object()
        order = income.order
        account = income.account
        order.status = 'inactive'
        order.paid_sum -= income.amount
        order.save()
        account.total_sum -= income.amount
        account.save()
        success_message = u"{} успішно видалене!".format(
            income)
        messages.success(self.request, success_message)
        return super(IncomeDelete, self).delete(
            self, request, *args, **kwargs)


def income_auto_create(detail):
    try:
        order = Order.objects.get(report=detail.report)
    except:
        order = order_auto_create(detail)
        order.save()
    new_income = {
        'order': order,
        'date': detail.date,
        'account': Account.objects.all().first(),
        'amount': detail.report.cost
    }
    return Income(**new_income)

def income_auto_edit(detail):
    return detail