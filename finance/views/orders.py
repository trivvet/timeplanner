# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..models import Order

@login_required(login_url='/login/')
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
        return HttpResponseRedirect(reverse('finance:accounts_list'))
    else:
        return render(request, 'finance/order_form.html', 
            {'header': header})

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
            new_order['tasks_number'] = int(tasks_number)
        except ValueError:
            new_order['tasks_number'] = tasks_number
            errors['tasks_number'] = u"Будь-ласка введіть ціле число"

    status = form_data.get('status')
    new_order['status'] = status

    return {'new_order': new_order, 'errors': errors}