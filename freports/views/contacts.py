# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from ..models import Contacts

status_list = {
    'judge': 'Суддя',
    'plaintiff': 'Позивач',
    'defendant': 'Відповідач',
    'plaintiff_agent': 'Представник позивача',
    'defendant_agent': 'Представник відповідача',
    'other_participant': 'Інший учасник'}

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
