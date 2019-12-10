# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required, 
    permission_required
    )
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from ..models import Contact

contacts_status_list = {
    'judge': u'Суддя',
    'member': u'Учасник справи',
    'participant': u'Представник',
    'lawyer': u"Адвокат",
    'customer': u"Замовник",
    'other': u"Інший"
}

status_translate = {
    'plaintiff': 'member',
    'defendant': 'member',
    'plaintiff_agent': 'participant',
    'defendant_agent': 'participant',
    'other_participant': 'other'
}

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def contacts_list(request):
    contacts = Contact.objects.all().order_by('surname')
    status = request.GET.get('status', '')
    if status == 'members':
        contacts = contacts.filter(status='member')
    elif status == 'customers':
        contacts = contacts.filter(status='customer')
    elif status == 'other':
        contacts = contacts.filter(status__in=[
            'participant', 'lawyer', 'other'])

    if request.GET.get('all_pages', '') == '':
        paginator = Paginator(contacts, 10)
        page = request.GET.get('page', '')
        try:
            contacts = paginator.page(page)
        except PageNotAnInteger:
            contacts = paginator.page(1)
        except EmptyPage:
            contacts = paginator.page(paginator.num_page)
    header = 'Список контактів'
    keys = contacts_status_list.keys()
    for contact in contacts:
        if contact.status in keys:
            contact.status = contacts_status_list[contact.status]
        elif contact.status in ['plaintiff', 'defendant', 'other_participant']:
            contact.status = u"Учасник справи"
        elif contact.status in ['plaintiff_agent', 'defendant_agent']:
            contact.status = u"Представник"
        else:
            contact.status = u"Невідомий статус"
    return render(request, 'freports/contacts_list.html', 
        {'contacts': contacts, 'header': header})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def contact_detail(request, cid):
    contact = Contact.objects.get(pk=cid)
    header = u"Детальна інформація про контакт {}".format(contact.surname)
    return render(request, 'freports/contact_detail.html', {
        'header': header, 'content': contact, 'status_list': contacts_status_list.iteritems()})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def add_contact(request):
    header='Додавання контакту'
    content = {}
    errors = {}

    if request.method == 'POST':
        if request.POST.get('save_button', ''):
            data = request.POST
            answer = valid_contact(data)
            contact = answer['contact']
            errors = answer['errors']
            if not errors:
                new_contact = Contact(**contact)
                new_contact.save()
                messages.success(request, 
                    u"Контакт {} успішно додано".format(new_contact.surname))
                return HttpResponseRedirect(reverse(
                    'freports:contacts_list'))
            messages.error(request, u"Виправте наступні помилки")
            content = contact

        elif request.POST.get('cancel_button', ''):
            messages.warning(request, u"Додавання контакту скасовано")
            return HttpResponseRedirect(reverse(
                'freports:contacts_list'))

    return render(request, 'freports/contact_form.html', {
        'header': header, 'status_list': contacts_status_list.iteritems(),
        'content': content, 'errors': errors})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def edit_contact(request, cid):
    contact = Contact.objects.get(pk=cid)
    header = u"Редагування контакту {}".format(contact.surname)
    errors = {}
    if request.method == 'POST':
        if request.POST.get('next_url', ''):
            next_url = request.POST.get('next_url')
        else:
            next_url = reverse('freports:contacts_list')
        if request.POST.get('save_button', ''):
            data = request.POST
            answer = valid_contact(data)
            edit_contact = answer['contact']
            errors = answer['errors']
            if not errors:
                edit_item = Contact(**edit_contact)
                edit_item.id = contact.id
                edit_item.save()
                messages.success(request, u"Контакт {} успішно змінено".format(edit_item.surname))
                return HttpResponseRedirect(next_url)
            else:
                messages.error(request, u"Виправте наступні помилки")
                content = edit_contact
        elif request.POST.get('cancel_button', ''):
            messages.warning(request, u"Редагування контакту скасовано")
            return HttpResponseRedirect(next_url)
    else:
        content = contact
        next_url = request.GET.get('next_url', '')

    return render(request, 'freports/contact_form.html', {
        'header': header, 'content': content, 'status_list': contacts_status_list.iteritems(),
        'errors': errors, 'next_url': next_url})


login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def delete_contact(request, cid):
    contact = Contact.objects.get(pk=cid)
    if request.method == 'POST':
        if request.POST.get('cancel_button', ''):
            messages.warning(request,
                u"Видалення контакту скасовано")
        elif request.POST.get('delete_button', ''):
            contact.delete()
            messages.success(request,
                u"Контакт {} {} успішно видалений".format(contact.surname, contact.name))
        return HttpResponseRedirect(reverse('freports:contacts_list'))
    else:
        header = u"Видалення контакту {}".format(contact.surname)
        content = u"Ви дійсно бажаєте видалити інформацію про контакт {} {}".format(contact.surname, contact.name)
        return render(request, 'freports/delete_form.html', 
            {'header': header, 'content': content})

def update_contacts_status(request):
    contacts = Contact.objects.all()
    for contact in contacts:
        if contact.status in status_translate.keys():
            contact.status = status_translate[contact.status]
            contact.save()
    messages.success(request,
                u"Статуси контактів успішно оновлено")
    return HttpResponseRedirect(reverse('freports:contacts_list'))

def valid_contact(data):
    errors = {}
    contact = {}

    surname = data.get('surname', '')
    if not surname:
        errors['surname'] = u"Прізвище є обов'язковим"
    else:
        contact['surname'] = surname

    name = data.get('name', '')
    if not name:
        errors['name'] = u"Ім'я та ім'я по-батькові є обов'язковим"
    else:
        contact['name'] = name

    status = data.get('status', '')
    if not status:
        errors['status'] = u"Статус є обов'язковим"
    else:
        if status in contacts_status_list.keys():
            contact['status'] = status
        else:
            errors['status'] = u"Виберіть статус зі списку"

    address = data.get('address', '')
    contact['address'] = address

    phone = data.get('phone', '')
    contact['phone'] = phone

    info = data.get('info')
    contact['info'] = info

    return {'errors': errors, 'contact': contact}