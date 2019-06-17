# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import date, timedelta

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import JsonResponse
from django.shortcuts import render
from django.views.generic.edit import (
    CreateView, 
    UpdateView, 
    DeleteView
    )
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator

from ..models import Execution, Order, Income
from ..forms import ExecutionForm


@login_required(login_url='/login/')
def executions_list(request):
    executions = Execution.objects.all().order_by('date').reverse()
    period = request.GET.get('period')
    now = timezone.now()
    start_current_month = date(now.year, now.month, 1)
    start_previous_month = date(now.year, now.month - 1, 1) - timedelta(days=1)
    start_current_year = date(now.year, 1, 1)
    start_previous_year = date(now.year - 1, 1, 1)
    if period == 'current_month':
        executions = executions.filter(date__gt=start_current_month - timedelta(days=1))
    elif period == 'previous_month':
        executions = executions.filter(date__gt=start_previous_month - timedelta(days=1)).filter(
            date__lt=start_current_month)
    elif period == 'current_year':
        executions = executions.filter(date__gt=start_current_year - timedelta(days=1))
    elif period == 'previous_year':
        executions = executions.filter(date__gt=start_previous_year - timedelta(days=1)).filter(
            date__lt=start_current_year)
    return render(request, 'finance/executions_list.html', 
        {'executions': executions})


@method_decorator(login_required, name='dispatch')
class ExecutionCreate(SuccessMessageMixin, CreateView):
    template_name = 'finance/form.html'
    form_class = ExecutionForm
    success_url = reverse_lazy('finance:executions_list')

    def get_context_data(self, **kwargs):
        context = super(ExecutionCreate, self).get_context_data(**kwargs)
        context['header'] = u"Додавання виконання"
        form = context['form']
        form.fields['order'].queryset = Order.objects.filter(
            status='active')
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
        account = data['account']
        order.done_sum += money
        if order.done_sum == order.total_sum:
            order.status = 'done'
        elif order.done_sum >= order.paid_sum:
            order.status = 'inactive'
        order.save()
        return super(ExecutionCreate, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        execution = self.object
        message = u"{} успішно додане!".format(
            execution)
        return message

@method_decorator(login_required, name='dispatch')
class ExecutionEdit(SuccessMessageMixin, UpdateView):
    model = Execution
    template_name = 'finance/form.html'
    form_class = ExecutionForm
    success_url = reverse_lazy('finance:executions_list')

    def get_context_data(self, **kwargs):
        context = super(ExecutionEdit, self).get_context_data(**kwargs)
        context['header'] = u"Редагування виконання"
        form = context['form']
        status = self.object.order.status
        form.fields['order'].queryset = Order.objects.filter(
            status=status)
        form.fields['order'].widget.attrs['disabled'] = 'disabled'
        
        return context
    
    def post(self, request, *args, **kwargs):
        execution_id = kwargs['pk']
        execution = Execution.objects.get(pk=execution_id)
        order_id = execution.order.id
        request.POST = request.POST.copy()
        request.POST['order'] = order_id
        return super(ExecutionEdit, 
            self).post(request, *args, **kwargs)

    def form_valid(self, form):
        data = form.cleaned_data
        initial_data = form.initial
        order = data['order']
        change_done_sum = data['amount'] - initial_data['amount']
        order.done_sum += change_done_sum
        if order.done_sum == order.total_sum:
            order.status = 'done'
        elif order.done_sum >= order.paid_sum:
            order.status = 'inactive'
        else:
            order.status = 'active'
        order.save()
        return super(ExecutionEdit, self).form_valid(form)

    def get_success_message(self, cleaned_data):
        execution = self.object
        message = u"{} успішно змінене!".format(
            execution)
        return message

@method_decorator(login_required, name='dispatch')
class ExecutionDelete(DeleteView):
    model = Execution
    template_name = 'finance/confirm_delete.html'
    success_url = reverse_lazy('finance:executions_list')

    def get_context_data(self, **kwargs):
        context = super(ExecutionDelete, self).get_context_data(**kwargs)
        context['header'] = u"Видалення виконання"
        return context

    def delete(self, request, *args, **kwargs):
        execution = self.get_object()
        order = execution.order
        order.status = 'active'
        order.done_sum -= execution.amount
        order.save()
        success_message = u"{} успішно видалене!".format(
            execution)
        messages.success(self.request, success_message)
        return super(ExecutionDelete, self).delete(
            self, request, *args, **kwargs)