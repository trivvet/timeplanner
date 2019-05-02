# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
from operator import attrgetter

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import DetailView

from ..models import Account, Income, Execution

@login_required(login_url='/login/')
def accounts_list(request):
    accounts = Account.objects.all().order_by('title')
    header = u'Список рахунків'
    return render(request, 'finance/accounts_list.html', 
        {'accounts': accounts, 'header': header})

class AccountDetail(DetailView):
    model = Account
    template_name = 'books/acme_list.html'
    template_name = 'finance/account_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AccountDetail, self).get_context_data(**kwargs)
        incomes = Income.objects.filter(account=self.object)
        executions = Execution.objects.filter(account=self.object)
        transactions = sorted(chain(incomes, executions),
            key=attrgetter('date'))
        context['transactions'] = transactions
        return context

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
                    {'header': header, 'errors': errors, 
                    'content': checked_data})
            else:
                new_account = Account(**checked_data)
                new_account.save()
                messages.success(request, 
                    u"Рахунок {} успішно доданий".format(new_account.title))
        else:
            messages.warning(request, u"Додавання рахунку скасовано")
        return HttpResponseRedirect(reverse('finance:accounts_list'))
    else:
        return render(request, 'finance/account_form.html', 
        {'header': header})

@login_required(login_url='/login/')
def edit_account(request, aid):
    header = u"Редагування рахунку"
    account = Account.objects.get(pk=aid)
    if request.method == 'POST':
        if request.POST.get('save_button', ''):
            info = valid_data(request.POST)
            checked_data = info['new_account']
            errors = info['errors']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'finance/account_form.html', 
                    {'header': header, 'errors': errors, 
                    'content': checked_data})
            else:
                edit_account = Account(**checked_data)
                edit_account.id = aid
                edit_account.save()
                messages.success(request, 
                    "Рахунок {} успішно змінений".format(
                        edit_account.title))
        elif request.POST.get('cancel_button', ''):
            messages.warning(request, "Редагування рахунку скасовано")
        return HttpResponseRedirect(reverse('finance:accounts_list'))
    else:
        return render(request, 'finance/account_form.html',
            {'header': header, 'content': account})
    
@login_required(login_url='/login/')
def delete_account(request, aid):
    account = Account.objects.get(pk=aid)
    header = u"Видалення рахунку"
    content = u"Ви дійсно бажаєте видалити рахунок {}?".format(
        account.title)
    if request.method == 'POST':
        if request.POST.get('delete_button', ''):
            account.delete()
            messages.success(request, 
                u"Рахунок {} успішно видалений".format(account.title))
        elif request.POST.get('cancel_button', ''):
            messages.warning(request,
                u"Видалення рахунку скасовано")
        return HttpResponseRedirect(reverse('finance:accounts_list'))
    else:
        return render(request, 'freports/delete_form.html',
            {'header': header, 'content': content})

def valid_data(form_data):
    new_account, errors = {}, {}
    title = form_data.get('title')
    if title:
        new_account['title'] = title
    else:
        errors['title'] = u"Назва рахунку є обов'язковою"

    total_sum = form_data.get('total_sum')
    if total_sum:
        try:
            new_account['total_sum'] = int(total_sum)
        except ValueError:
            new_account['total_sum'] = total_sum
            errors['total_sum'] = u"Будь-ласка введіть ціле число"
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
