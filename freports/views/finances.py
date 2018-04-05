# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from ..models import Account

# import pytz, datetime
# from datetime import date, datetime, timedelta
# from calendar import day_abbr

# from django.shortcuts import render
# from django.http import HttpResponseRedirect
# from django.urls import reverse
# from django.utils import translation
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required
# from django.utils.timezone import get_current_timezone, localtime
# from django.utils.formats import date_format

# from ..models import Task, Report, ReportEvents, ReportSubject

@login_required(login_url='/login/')
def accounts_list(request):
    accounts = Account.objects.all().order_by('title')
    header = u'Список рахунків'
    return render(request, 'freports/accounts_list.html', 
        {'accounts': accounts, 'header': header})

@login_required(login_url='/login/')
def add_account(request):
    header = u'Додавання рахунку'
    if request.method == 'POST':
        return render(request, 'freports/account_form.html', 
        {'header': header})
    else:
        return render(request, 'freports/account_form.html', 
        {'header': header})

