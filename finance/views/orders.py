# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required, 
    permission_required
    )
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from ..models import Order, Income, Execution

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def orders_list(request):
    orders = Order.objects.all().order_by('name')
    orders_active = orders.filter(status='active')
    orders_inactive = orders.filter(status='inactive')
    orders_done = orders.filter(status='done')
    content = {
        'total_sum': 0,
        'paid_sum': 0,
        'done_sum': 0,
        'remainder_sum': 0,
        'all_orders': orders.count(),
        'active_orders': orders_active.count(),
        'inactive_orders': orders_inactive.count(),
        'done_orders': orders_done.count()
    }
    status = request.GET.get('status', '')
    if status == 'inactive':
        orders = orders_inactive
    elif status == 'done':
        orders = orders_done
    elif not request.GET.get('status', ''):
        orders = orders_active
    for order in orders:
        content['total_sum'] += order.total_sum
        content['paid_sum'] += order.paid_sum
        content['done_sum'] += order.done_sum
        content['remainder_sum'] += order.remainder
    return render(request, 'finance/orders_list.html', 
        {'orders': orders, 'content': content})

@method_decorator(login_required, name='dispatch')
class OrderDetail(ListView):
    model = Order
    template_name = 'finance/order_detail.html'

    def get_queryset(self):
        order = self.kwargs['pk']
        incomes = Income.objects.filter(order=order)
        executions = Execution.objects.filter(order=order)
        object_list = sorted(chain(incomes, executions),
            key=attrgetter('date'), reverse=True)
        return object_list

    def get_context_data(self, **kwargs):
        context = super(OrderDetail, self).get_context_data(**kwargs)
        order = self.kwargs['pk']
        context['object'] = Order.objects.get(pk=order)
        return context

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def add_order(request):
    header = u"Додавання замовлення"
    if request.method == 'POST':
        if request.POST.get('save_button', ''):
            info = valid_data(request.POST)
            checked_data = info['new_order']
            errors = info['errors']
            if errors:
                messages.error(request, 
                    u"Виправте наступні помилки")
                return render(request, 'finance/order_form.html', 
                    {'header': header, 'errors': errors, 
                    'item': checked_data})
            else:
                new_order = Order(**checked_data)
                new_order.save()
                messages.success(request,
                    u"{} успішно додано!".format(
                        new_order))
        elif request.POST.get('cancel_button', ''):
            messages.warning(request, 
                u"Додавання замовлення скасовано")
        return HttpResponseRedirect(reverse('finance:orders_list'))
    else:
        return render(request, 'finance/order_form.html', 
            {'header': header})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def edit_order(request, oid):
    header = u"Редагування замовлення"
    order = Order.objects.get(pk=oid)
    if request.method == 'POST':
        if request.POST.get('save_button', ''):
            info = valid_data(request.POST)
            checked_data = info['new_order']
            errors = info['errors']
            if errors:
                messages.error(request,
                    u"Випавте наступні помилки")
                return render(request, 'finance/order_form.html',
                    {'header': header, 'errors': errors,
                     'item': checked_data})
            else:
                edit_order = Order(**checked_data)
                edit_order.id = order.id
                edit_order.report = order.report
                edit_order.save()
                messages.success(request, 
                    u"{} успішно змінене".format(
                        edit_order))
        elif request.POST.get('cancel_button', ''):
            messages.warning(request,
                u"Редагування замовлення скасовано")
        return HttpResponseRedirect(reverse('finance:orders_list'))
    else:
        return render(request, 'finance/order_form.html',
            {'header': header, 'item': order})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def delete_order(request, oid):
    order = Order.objects.get(pk=oid)
    header = u"Видалення замовлення"
    content = u"Ви дійсно бажаєте видалити {}".format(order)
    if request.method == 'POST':
        if request.POST.get('delete_button', ''):
            order.delete()
            messages.success(request, 
                u"{} успішно видалене".format(order))
        elif request.POST.get('cancel_button', ''):
            messages.warning(request,
                u"Видалення замовлення скасовано")
        return HttpResponseRedirect(reverse('finance:orders_list'))
    else:
        return render(request, 'freports/delete_form.html',
            {'header': header, 'content': content})

def valid_data(form_data):
    new_order, errors = {}, {}
    name = form_data.get('name')
    if name:
        new_order['name'] = name
    else:
        errors['name'] = u"Назва замовлення є обов'язковою"

    total_sum = form_data.get('total_sum')
    if total_sum:
        try:
            new_order['total_sum'] = int(total_sum)
        except ValueError:
            new_order['total_sum'] = total_sum
            errors['total_sum'] = u"Будь-ласка введіть ціле число"
    else:
        errors['total_sum'] = u"Кошторисна вартість є обов'язковою"

    paid_sum = form_data.get('paid_sum')
    if paid_sum:
        try:
            new_order['paid_sum'] = int(paid_sum)
        except ValueError:
            new_order['paid_sum'] = paid_sum
            errors['paid_sum'] = u"Будь-ласка введіть ціле число"

    done_sum = form_data.get('done_sum')
    if done_sum:
        try:
            new_order['done_sum'] = int(done_sum)
        except ValueError:
            new_order['done_sum'] = done_sum
            errors['done_sum'] = u"Будь-ласка введіть ціле число"

    tasks_number = form_data.get('tasks_number')
    if tasks_number:
        try:
            new_order['tasks_number'] = float(tasks_number.replace(",", '.'))
        except ValueError:
            new_order['tasks_number'] = tasks_number
            errors['tasks_number'] = u"Будь-ласка введіть число"

    status = form_data.get('status')
    new_order['status'] = status

    return {'new_order': new_order, 'errors': errors}

def order_auto_create(detail):
    new_order = {
        'name': u'Висновок №{}'.format(detail.report.full_number()),
        'report': detail.report,
        'total_sum': detail.cost,
        'status': 'inactive'
    }
    return Order(**new_order)

def order_auto_edit(detail):
    try:
        edit_order = Order.objects.get(report=detail.report)
        edit_order.total_sum = detail.cost
    except:
        edit_order = order_auto_create(detail)
    return edit_order