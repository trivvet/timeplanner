# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from ..models import Contacts

@login_required(login_url='/login/')
def contacts_list(request):
    contacts = Contacts.objects.all().order_by('surname')
    header = 'Список контактів'
    return render(request, 'freports/contacts_list.html', {'contacts': contacts, 'header': header})
