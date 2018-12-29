# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from ..models import Execution


@login_required(login_url='/login/')
def executions_list(request):
    executions = Execution.objects.all()
    return render(request, 'finance/executions_list.html', 
        {'executions': executions})