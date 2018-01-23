# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.signals import user_login_failed
from django.contrib.auth.models import User

from axes.models import AccessAttempt
from axes.utils import reset

attempt = AccessAttempt.objects.all()

def login_auth(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # import pdb;pdb.set_trace()
        if attempt.count() > 0 and attempt[0].failures > 5:
            messages.error(request, "Кількість спроб перевищела допустиму, спробуйте пізніше")
            return render(request, 'freports/login_form.html', {})
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            reset()
            # user_logged_in.
            messages.success(request, "Ви успішно увійшли як %s" % username)
            return HttpResponseRedirect(reverse('forensic_reports_list'))
        else:
            # import pdb;pdb.set_trace()
            user_login_failed.send(
                sender = User,
                request = request,
                credentials = {
                    'username': username
                },
            )
            messages.error(request, "Невірно введене ім'я користувача або пароль")

    return render(request, 'freports/login_form.html', {})

def logout_auth(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_form'))
