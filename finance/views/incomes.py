# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib import messages
from django import forms
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

from ..models import Income, Order
from ..forms import IncomeForm

@login_required(login_url='/login/')
def incomes_list(request):
    incomes = Income.objects.all()
    return render(request, 'finance/incomes_list.html', 
        {'incomes': incomes})

@method_decorator(login_required, name='dispatch')
class IncomeCreate(CreateView):
    template_name = 'finance/form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('finance:incomes_list')

    def get_context_data(self, **kwargs):
        context = super(IncomeCreate, self).get_context_data(**kwargs)
        context['header'] = u"Додавання надходження"
        return context

    def render_to_response(self, context):
        # import pdb;pdb.set_trace()
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            order_id = self.request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
            return JsonResponse(
                {'total_sum': order.total_sum}
            )
        else:
            return super(IncomeCreate, self).render_to_response(context)

@method_decorator(login_required, name='dispatch')
class IncomeEdit(UpdateView):
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
        # import pdb;pdb.set_trace()
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            order_id = self.request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
            return JsonResponse(
                {'total_sum': order.total_sum}
            )
        else:
            return super(IncomeEdit, self).render_to_response(context)

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
        return super(IncomeDelete, self).delete(
            self, request, *args, **kwargs)