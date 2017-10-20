# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

from ..models import Report, ReportDetails

def login_auth(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Ви успішно увійшли як %s" % username)
            return HttpResponseRedirect(reverse('forensic_reports_list'))
        else:
            messages.error(request, "Невірно введене ім'я користувача або пароль")

    return render(request, 'freports/login_form.html', {})

def logout_auth(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_form'))
