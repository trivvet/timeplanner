# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from ..models import Judge

@login_required(login_url='/login/')
def judges_list(request):
    judges = Judge.objects.all().order_by('surname')
    header = 'Список суддів'
    return render(request, 'freports/judges_list.html', {'judges': judges, 'header': header})

@login_required(login_url='/login/')
def add_court(request):
    header = u'Додавання суду'
    return render(request, 'freports/court_form.html', {'header': header})
