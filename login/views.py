# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, signals
from django.contrib.auth.decorators import (
    login_required, 
    permission_required
    )
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import timezone

from axes.models import AccessAttempt, AccessLog

def login_auth(request):
    attempts = AccessAttempt.objects.all()
    login_attempts_last = 0
    if attempts:
        login_attempts_last = attempts[0].failures_since_start

    if login_attempts_last > 3:
        messages.error(request, 
            "Кількість спроб перевищила допустиму, спробуйте пізніше")
        return render(request, 'login/form_locked.html', {})

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = authenticate(request, username=username, 
                password=password)
        
            if user is not None:
                login(request, user)
                messages.success(request, 
                    "Ви успішно увійшли як %s" % username)
                return HttpResponseRedirect(
                    reverse('freports:reports_list'))
            else:
                messages.error(request, 
                    u"Невірно введене ім'я користувача або пароль")
                login_attempts_last += 1
        except UnicodeEncodeError:
            messages.error(request,
                u"Некоректно введене ім'я користувача або пароль")
            login_attempts_last += 1

    return render(request, 'login/form.html', {})

def logout_auth(request):
    logs = AccessLog.objects.all()
    logs.last().logout_time = timezone.now()
    logout(request)
    return HttpResponseRedirect(reverse('login:form'))

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def login_attempts(request):
    attempts_all = AccessAttempt.objects.all()
    attempts = attempts_all
    for attempt in attempts:
        attempt.new_post_data = attempt.post_data.split('---------')
    return render(request, 'login/attempts.html', 
        {'attempts': attempts})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def login_logs(request):
    logs = AccessLog.objects.all().order_by('attempt_time').reverse()
    if request.GET.get('all_pages', '') == '':
        paginator = Paginator(logs, 8)
        page = request.GET.get('page', '')
        try:
            logs = paginator.page(page)
        except PageNotAnInteger:
            logs = paginator.page(1)
        except EmptyPage:
            logs = paginator.page(paginator.num_page)
    return render(request, 'login/logs.html', 
        {'logs': logs})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def delete_old_attempts(request):
    attempts = AccessAttempt.objects.all()
    old_logs = 0
    for attempt in attempts:
        substract = timezone.now().date() - attempt.attempt_time.date()
        if substract.days > 31:
            attempt.delete()
            old_logs += 1
    if old_logs > 0:
        messages.success(request, 
            u"Логи, записані більше місяця тому, успішно видалено")
    else:
        messages.warning(request,
            u"Давніх спроб входу не виявлено")
    return HttpResponseRedirect(reverse('login:attempts'))