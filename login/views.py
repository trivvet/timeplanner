# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from axes.models import AccessAttempt

def login_auth(request):
    attempts = AccessAttempt.objects.all()
    login_attempts_last = 0
    if attempts:
        login_attempts_last = attempts[0].failures

    if login_attempts_last > 2:
        messages.error(request, 
            "Кількість спроб перевищила допустиму, спробуйте пізніше")
        return render(request, 'freports/login_form_locked.html', {})

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, 
            password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 
                "Ви успішно увійшли як %s" % username)
            return HttpResponseRedirect(
                reverse('forensic_reports_list'))
        else:
            messages.error(request, 
                "Невірно введене ім'я користувача або пароль")
            login_attempts_last += 1

    return render(request, 'freports/login_form.html', {})

def logout_auth(request):
    logout(request)
    return HttpResponseRedirect(reverse('login_form'))

@login_required(login_url='/login/')
def login_attempts(request):
    attempts = AccessAttempt.objects.all()
    return render(request, 'freports/login_attempts.html', 
        {'attempts': attempts})

@login_required(login_url='/login/')
def delete_old_attempts(request):
    attempts = Task.objects.all()
    for attempt in attempts:
        substract = timezone.now().date() - task.time.date()
        if substract.days > 31:
            task.delete()
    messages.success(request, 
        u"Завдання, виконані більше місяця тому, успішно видалено")
    return HttpResponseRedirect(reverse('tasks_list'))
