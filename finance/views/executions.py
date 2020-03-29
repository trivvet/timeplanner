# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, datetime, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import F
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView
    )
from django.views.generic.list import ListView
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator

from .incomes import filter_by_date
from ..models import Execution, Order, Income
from ..forms import ExecutionForm

@method_decorator(login_required, name='dispatch')
class ExecutionList(SuccessMessageMixin, ListView):
    model = Execution
    context_object_name = 'executions'
    template_name = "finance/executions_list.html"
    ordering = '-date'
    paginate_by = 15

    def get_queryset(self):
        executions = super(ExecutionList, self).get_queryset()
        return filter_by_date(self, executions)['items']

    def get_context_data(self, **kwargs):
        all_pages = self.request.GET.get("all_pages", '')
        context = super(ExecutionList, self).get_context_data(**kwargs)
        if all_pages:
            executions = Execution.objects.all().order_by('-date')
            context['executions'] = filter_by_date(self, executions)['items']
            context['is_paginated'] = False
        context['errors'] = filter_by_date(self)['errors']
        return context

@method_decorator(login_required, name='dispatch')
class ExecutionCreate(SuccessMessageMixin, CreateView):
    template_name = 'finance/form.html'
    form_class = ExecutionForm

    def get_context_data(self, **kwargs):
        context = super(ExecutionCreate, self).get_context_data(**kwargs)
        context['header'] = u"Додавання виконання"
        order = self.request.GET.get('order')
        form = context['form']
        if order:
            form.fields['order'].queryset = Order.objects.filter(
                pk=order)
            form.fields['order'].initial = order
            form.fields['order'].empty_label = None
            form.fields['amount'].initial = Order.objects.get(
                pk=order).remainder
            incomes = Income.objects.filter(order=order)
            form.fields['account'].initial = incomes[0].account
        else:
            form.fields['order'].queryset = Order.objects.filter(
                done_sum__lt=F('paid_sum')).order_by('name')
        return context

    def render_to_response(self, context):
        if self.request.GET.get('format') == 'json':
            order_id = self.request.GET.get('order_id')
            order = Order.objects.get(pk=order_id)
            incomes = Income.objects.filter(
                order=order).order_by('date').reverse()
            # import pdb;pdb.set_trace()
            if incomes:
                account_id = incomes[0].account.id
            else:
                account_id = ""
            done_sum = order.paid_sum - order.done_sum
            return JsonResponse(
                {'total_sum': done_sum,
                 'account_id': account_id,
                 'tasks_number': order.tasks_number}
            )
        else:
            return super(ExecutionCreate, self).render_to_response(
                context)

    def form_valid(self, form):
        data = form.cleaned_data
        money = int(data['amount'])
        order = data['order']
        order.done_sum += money
        order.save()
        return super(ExecutionCreate, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        execution = self.object
        order = self.request.GET.get('order')
        if order:
            message = u"Виконання успішно додане"
        else:
            message = u"{} успішно додане!".format(
                execution)
        return message

    def get_success_url(self):
        if self.request.GET.get('order'):
            success_url = reverse_lazy('finance:detail_order', kwargs={'pk': self.object.order.id})
        else:
            success_url = reverse_lazy('finance:executions_list')
        return success_url


@method_decorator(login_required, name='dispatch')
class ExecutionEdit(SuccessMessageMixin, UpdateView):
    model = Execution
    template_name = 'finance/form.html'
    form_class = ExecutionForm

    def get_context_data(self, **kwargs):
        context = super(ExecutionEdit, self).get_context_data(**kwargs)
        context['header'] = u"Редагування виконання"
        form = context['form']
        initial = context['object']
        form.fields['order'].queryset = Order.objects.filter(pk=initial.order.id)
        form.fields['order'].empty_label = None
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        initial_data = form.initial
        order = data['order']
        change_done_sum = data['amount'] - initial_data['amount']
        order.done_sum += change_done_sum
        order.save()
        return super(ExecutionEdit, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        execution = self.object
        next_url = self.request.GET.get('next_url')
        if next_url:
            message = u"Виконання успішно змінене"
        else:
            message = u"{} успішно змінене!".format(
                execution)
        return message

    def get_success_url(self):
        if self.request.GET.get('next_url') == 'detail_order':
            success_url = reverse_lazy('finance:detail_order', kwargs={'pk': self.object.order.id})
        else:
            success_url = reverse_lazy('finance:executions_list')
        return success_url

@method_decorator(login_required, name='dispatch')
class ExecutionDelete(DeleteView):
    model = Execution
    template_name = 'finance/confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(ExecutionDelete, self).get_context_data(**kwargs)
        context['header'] = u"Видалення виконання"
        return context

    def delete(self, request, *args, **kwargs):
        execution = self.get_object()
        order = execution.order
        order.done_sum -= execution.amount
        order.save()
        next_url = request.GET.get('next_url')
        if next_url:
            success_message = u"Виконання успішно видалене!"
        else:
            success_message = u"{} успішно видалене!".format(
                execution)
        messages.success(self.request, success_message)
        return super(ExecutionDelete, self).delete(
            self, request, *args, **kwargs)

    def get_success_url(self):
        if self.request.GET.get('next_url') == 'detail_order':
            success_url = reverse_lazy('finance:detail_order', kwargs={'pk': self.object.order.id})
        else:
            success_url = reverse_lazy('finance:executions_list')
        return success_url