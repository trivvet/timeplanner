# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import Account, Order

@login_required(login_url='/login/')
def accounts_list(request):
    accounts = Account.objects.all().order_by('title')
    orders = Order.objects.all()
    content = {}
    content['total_sum'] = 0
    content['paid_sum'] = 0
    content['done_sum'] = 0
    for order in orders:
        content['total_sum'] += order.total_sum
        content['paid_sum'] += order.paid_sum
        content['done_sum'] += order.done_sum
    header = u'Список рахунків'
    return render(request, 'finance/accounts_list.html', 
        {'accounts': accounts, 'header': header, 'orders': orders,
         'content': content})

@login_required(login_url='/login/')
def add_account(request):
    header = u'Додавання рахунку'
    if request.method == 'POST':
        if request.POST.get('save_button'):
            info = valid_data(request.POST)
            checked_data = info['new_account']
            errors = info['errors']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'finance/account_form.html', 
                    {'header': header, 'errors': errors, 'content': checked_data})
            else:
                new_account = Account(**checked_data)
                new_account.save()
                messages.success(request, u"Рахунок {} успішно доданий".format(new_account.title))
        else:
            messages.warning(request, u"Додавання рахунку скасовано")
        return HttpResponseRedirect(reverse('finance:accounts_list'))
    else:
        return render(request, 'finance/account_form.html', 
        {'header': header})

def valid_data(form_data):
    new_account, errors = {}, {}
    title = form_data.get('title')
    if title:
        new_account['title'] = title
    else:
        errors['title'] = u"Назва рахунку є обов'язковою"

    total_sum = form_data.get('total_sum')
    if total_sum:
        new_account['total_sum'] = total_sum
    else:
        errors['total_sum'] = u"Сума на рахунку є обов'язковою"

    credit_cash = form_data.get('credit_cash')
    if credit_cash:
        try:
            new_account['credit_cash'] = int(credit_cash)
        except ValueError:
            new_account['credit_cash'] = credit_cash
            errors['credit_cash'] = u"Будь-ласка введіть ціле число"

    cash = form_data.get('cash')
    if cash:
        new_account['cash'] = True
    else:
        new_account['cash'] = False

    status = form_data.get('status')
    new_account['status'] = status

    return {'new_account': new_account, 'errors': errors}
