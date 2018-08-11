# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from ..models import Contacts

status_list = {
    'judge': 'Суддя',
    'plaintiff': 'Позивач',
    'defendant': 'Відповідач',
    'plaintiff_agent': 'Представник позивача',
    'defendant_agent': 'Представник відповідача',
    'other_participant': 'Інший учасник',
    u'': 'adfjlakjf'}

@login_required(login_url='/login/')
def contacts_list(request):
    contacts = Contacts.objects.all().order_by('surname')
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
    for contact in contacts:
        contact.status = status_list[contact.status]
    return render(request, 'freports/contacts_list.html', {'contacts': contacts, 'header': header})

@login_required(login_url='/login/')
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
                new_contact = Contacts(**contact)
                new_contact.save()
                messages.success(request, 
                    u"Контакт {} успішно додано".format(new_contact.surname))
                return HttpResponseRedirect(reverse('contacts_list'))
            messages.error(request, u"Виправте наступні помилки")
            content = contact

        elif request.POST.get('cancel_button', ''):
            messages.warning(request, u"Додавання контакту скасовано")
            return HttpResponseRedirect(reverse('contacts_list'))

    return render(request, 'freports/contact_form.html', {
        'header': header, 'status_list': status_list.iteritems(),
        'content': content, 'errors': errors})

login_required(login_url='/login/')
def delete_contact(request, cid):
    contact = Contacts.objects.get(pk=cid)
    if request.method == 'POST':
        if request.POST.get('cancel_button', ''):
            messages.warning(request,
                u"Видалення контакту скасовано")
        elif request.POST.get('delete_button', ''):
            contact.delete()
            messages.success(request,
                u"Контакт {} {} успішно видалений".format(contact.surname, contact.name))
        return HttpResponseRedirect(reverse('contacts_list'))
    else:
        header = u"Видалення контакту {}".format(contact.surname)
        content = u"Ви дійсно бажаєте видалити інформацію про контакт {} {}".format(contact.surname, contact.name)
        return render(request, 'freports/delete_form.html', 
            {'header': header, 'content': content})

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
        if status in status_list.keys():
            contact['status'] = status
        else:
            errors['status'] = u"Виберіть статус зі списку"

    address = data.get('address', '')

    phone = data.get('phone', '')
    if not phone:
        errors['phone'] = u"Номер телефону є обов'язковим"
    else:
        contact['phone'] = phone

    info = data.get('info')

    return {'errors': errors, 'contact': contact}