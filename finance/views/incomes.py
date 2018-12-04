# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse
from django.utils.decorators import method_decorator

from ..models import Income
from ..forms import IncomeForm

@login_required(login_url='/login/')
def incomes_list(request):
    incomes = Income.objects.all()
    return render(request, 'finance/incomes_list.html', 
        {'incomes': incomes})

@method_decorator(login_required, name='dispatch')
class IncomeCreate(CreateView):
    template_name = 'finance/form.html'
    form_class = IncomeForm
