# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_login_failed, user_logged_in, user_logged_out
from django.contrib.auth.models import User

from axes.models import AccessAttempt
from axes.utils import reset

def login_auth(request):
    attempts = AccessAttempt.objects.all()
    login_attempts_last = 0
    if attempts:
        login_attempts_last = attempts[0].failures

    if login_attempts_last > 2:
        messages.error(request, "Кількість спроб перевищила допустиму, спробуйте пізніше")
        return render(request, 'freports/login_form_locked.html', {})

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
            login_attempts_last += 1

    return render(request, 'freports/login_form.html', {})

def logout_auth(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_form'))

def login_attempts(request):
    attempts = AccessAttempt.objects.all()
    return render(request, 'freports/login_attempts.html', {'attempts': attempts})
