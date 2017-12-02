# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

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
    header = 'Список контактів'
    for contact in contacts:
        contact.status = status_list[contact.status]
    return render(request, 'freports/contacts_list.html', {'contacts': contacts, 'header': header})
