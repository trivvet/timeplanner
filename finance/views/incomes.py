# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from ..models import Income

@login_required(login_url='/login/')
def incomes_list(request):
    incomes = Income.objects.all()
    return render(request, 'finance/incomes_list.html', 
        {'incomes': incomes})