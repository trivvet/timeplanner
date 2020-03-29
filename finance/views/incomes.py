# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, datetime, timedelta

from django import forms
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import F
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView
    )
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator

from ..models import Income, Order, Account
from ..forms import IncomeForm
from . import order_auto_create

@method_decorator(login_required, name='dispatch')
class IncomeList(ListView):
    model = Income
    context_object_name = 'incomes'
    template_name = 'finance/incomes_list.html'
    ordering = '-date'
    paginate_by = 15

    def get_queryset(self):
        incomes = super(IncomeList, self).get_queryset()
        return filter_by_date(self, incomes)['items']

    def get_context_data(self, **kwargs):
        all_pages = self.request.GET.get("all_pages", '')
        context = super(IncomeList, self).get_context_data(**kwargs)
        if all_pages:
            incomes = Income.objects.all().order_by('-date')
            context['incomes'] = filter_by_date(self, incomes)['items']
            context['is_paginated'] = False
        context['errors'] = filter_by_date(self)['errors']
        return context

@method_decorator(login_required, name='dispatch')
class IncomeCreate(SuccessMessageMixin, CreateView):
    template_name = 'finance/form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('finance:incomes_list')

    def get_context_data(self, *args, **kwargs):
        context = super(IncomeCreate, self).get_context_data(**kwargs)
        context['header'] = u"Додавання надходження"
        order = self.request.GET.get('order')
        form = context['form']
        if order:
            form.fields['order'].queryset = Order.objects.filter(
                pk=order)
            form.fields['order'].initial = order
            form.fields['order'].empty_label = None
            form.fields['amount'].initial = Order.objects.get(
                pk=order).unpaid_sum
        else:
            form.fields['order'].queryset = Order.objects.filter(
                paid_sum__lt=F('total_sum')).order_by('name')
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
        order.paid_sum += money
        order.save()
        return super(IncomeCreate, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        income = self.object
        order = self.request.GET.get('order')
        if order:
            message = u"Надходження успішно додане"
        else:
            message = u"{} успішно додане!".format(
                income)
        return message

    def get_success_url(self):
        order = self.request.GET.get('order')
        if order:
            return reverse('finance:detail_order', 
                kwargs={'pk': order})
        else:
            return super(IncomeCreate, self).get_success_url()

@method_decorator(login_required, name='dispatch')
class IncomeEdit(SuccessMessageMixin, UpdateView):
    model = Income
    template_name = 'finance/form.html'
    form_class = IncomeForm

    def get_context_data(self, **kwargs):
        context = super(IncomeEdit, self).get_context_data(**kwargs)
        context['header'] = u"Редагування надходження"
        initial = context['object']
        form = context['form']
        form.fields['order'].queryset = Order.objects.filter(pk=initial.order.id)
        form.fields['order'].empty_label = None
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

    def form_valid(self, form):
        data = form.cleaned_data
        initial_data = form.initial
        if data['amount'] != initial_data['amount']:
            difference_sum = data['amount'] - initial_data['amount']
            data['order'].paid_sum += difference_sum
            data['order'].save()
        return super(IncomeEdit, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        income = self.object
        order = self.request.GET.get('next_url')
        if order:
            message = u"Надходження успішно змінене"
        else:
            message = u"{} успішно змінене!".format(
                income)
        return message

    def get_success_url(self):
        if self.request.GET.get('next_url') == 'detail_order':
            success_url = reverse_lazy('finance:detail_order', kwargs={'pk': self.object.order.id})
        else:
            success_url = reverse_lazy('finance:incomes_list')
        return success_url

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
        order.paid_sum -= income.amount
        order.save()
        next_url = request.GET.get('next_url')
        if next_url:
            success_message = u"Надходження успішно видалене"
        else:
            success_message = u"{} успішно видалене!".format(
                income)
        messages.success(self.request, success_message)
        return super(IncomeDelete, self).delete(
            self, request, *args, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('next_url') == 'detail_order':
            success_url = reverse_lazy('finance:detail_order', kwargs={'pk': self.object.order.id})
        else:
            success_url = reverse_lazy('finance:incomes_list')
        return success_url


def income_auto_create(detail):
    detail.cost = detail.report.cost
    try:
        order = Order.objects.get(report=detail.report)
        if not detail.cost:
            detail.cost = order.total_sum
    except:
        if not detail.cost:
            detail.cost = 10000
        order = order_auto_create(detail)
        order.save()
    if detail.subspecies == 'bank':
        print 'bank'
        account = Account.objects.filter(status='work', cash=False)
    else:
        print 'cash'
        account = Account.objects.filter(status='work', cash=True)
    new_income = {
        'order': order,
        'date': detail.date,
        'account': Account.objects.all().first(),
        'amount': detail.cost
    }
    return Income(**new_income)

def income_auto_edit(detail):
    return detail

def filter_by_date(self, items=None):
    period = self.request.GET.get('period')
    errors = {}
    now = timezone.now()
    start_current_month = date(now.year, now.month, 1)
    if now.month > 1:
        start_previous_month = date(now.year, 
            now.month - 1 or 1, 1) - timedelta(days=1)
    else:
        start_previous_month = date(
            now.year - 1, 12, 1)- timedelta(days=1)
    start_current_year = date(now.year, 1, 1)
    start_previous_year = date(now.year - 1, 1, 1)
    date_from = self.request.GET.get('date_from')
    date_until = self.request.GET.get('date_until')
    filter_status = self.request.GET.get('filter_status')
    if filter_status and date_from and date_until:
        date_from_datetime = datetime.strptime(date_from, '%Y-%m-%d')
        date_until_datetime = datetime.strptime(date_until, '%Y-%m-%d')
        if items:
            items = items.filter(date__gt=date_from_datetime - timedelta(days=1), 
                date__lt=date_until_datetime + timedelta(days=1))
        if date_from_datetime > date_until_datetime:
             errors = {'wrong_date': True}
    elif filter_status:
        errors = {'miss_date': True}
    else:
        if period == 'current_month' and items:
            items = items.filter(date__gt=start_current_month - timedelta(days=1))
        elif period == 'previous_month' and items:
            items = items.filter(
                date__gt=start_previous_month - timedelta(days=1),
                date__lt=start_current_month)
    return {'items': items, 'errors': errors}