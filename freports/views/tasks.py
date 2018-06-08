# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz, datetime
from datetime import date, datetime, timedelta
from calendar import day_abbr

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.utils import translation
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import get_current_timezone, localtime
from django.utils.formats import date_format

from ..models import Task, Report, ReportEvents, ReportSubject

@login_required(login_url='/login/')
def tasks_list(request):
    tasks = Task.objects.all().order_by('time')
    header = u'Список завдань'
    return render(request, 'freports/tasks_list.html', 
    	{'tasks': tasks, 'header': header})

@login_required(login_url='/login/')
def tasks_today_list(request):
    today = date.today()
    tasks = Task.objects.filter(time__startswith=today)
    translation.activate('uk')
    header = u'{} {}'.format(date_format(today, 'l'), today.strftime("%d-%m-%Y"))
    return render(request, 'freports/tasks_today_list.html',
        {'tasks': tasks, 'header': header})


@login_required(login_url='/login/')
def add_task(request):
    header = u'Додавання завдання'
    reports = Report.objects.filter(executed=False).order_by('number')
    if request.method == 'POST':
        if request.POST.get('save_button'):
            valid_data = valid_task(request.POST)
            errors = valid_data['errors']
            new_task = valid_data['new_task']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/task_form.html', 
                    {'content': new_task, 'errors': errors, 'header': header, 'reports': reports})
            else:
                new_item = Task(**new_task)
                new_item.save()
                messages.success(request, u"Завдання %s успішно додане" % new_item)
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання завдання скасовано")

        return HttpResponseRedirect(reverse('tasks_list'))

    else:
        return render(request, 'freports/task_form.html', {'header': header, 'reports': reports})

def add_detail_task(detail):
    new_task = valid_detail_task(detail)
    if new_task['valid']:
        new_item = Task(**new_task['task_data'])
        new_item.save()
    return HttpResponseRedirect(reverse('tasks_list'))

@login_required(login_url='/login/')
def edit_task(request, tid):
    task = Task.objects.get(pk=tid)
    header = u'Редагування інформації про завдання {name} яке призначене на {date}'.format(
        name=task.kind, date=task.time.strftime("%Y-%m-%d"))
    reports = Report.objects.filter(executed=False).order_by('number')
    if request.method == 'POST':
        if request.POST.get('save_button'):
            valid_data = valid_task(request.POST)
            errors = valid_data['errors']
            edit_task = valid_data['new_task']
            if errors:
                if errors['event']:
                    messages.error(request, errors['event'])
                else:
                    messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/task_form.html',
                    {'content': edit_task, 'errors': errors, 'header': header, 'reports': reports})
            else:
                edit_item = Task(**edit_task)
                edit_item.id = task.id
                edit_item.save()
                messages.success(request, u"Завдання {} успішно змінене".format(edit_item.kind))
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Радагування завдання скасовано")

        return HttpResponseRedirect(reverse('tasks_list'))
    else:
        task.time = localtime(task.time).isoformat()
        return render(request, 'freports/task_form.html', 
            {'header': header, 'content': task, 'reports': reports})

def edit_detail_task(detail):
    edit_task = Task.objects.filter(event=detail)
    new_task = valid_detail_task(detail)
    if new_task['valid']:
        new_item = Task(**new_task['task_data'])
        if edit_task:
            new_item.id = edit_task[0].id
        new_item.save()
    return HttpResponseRedirect(reverse('tasks_list'))

@login_required(login_url='/login/')
def delete_task(request, tid):
    task = Task.objects.get(pk=tid)
    if request.method == 'POST':
        if request.POST.get('delete_button'):
            task.delete()
            messages.success(request, u"Завдання успішно видалене")
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання завдання скасовано")
        return HttpResponseRedirect(reverse('tasks_list'))
    else:
        header = u'Видалення завдання'
        content = u"Ви дійсно бажаєте видалити інформацію про завдання {name} яке призначене на {date}?".format(
            name=task.kind, date=task.time.strftime("%Y-%m-%d"))
        return render(request, 'freports/delete_form.html', 
            {'content': content, 'header': header})

def valid_task(request_info):
    errors, new_task = {}, {}
    kind = request_info['kind']
    if not kind:
        errors['kind'] = u"Вид завдання є обов'язковим"
    else:
        new_task['kind'] = kind
    
    time = request_info.get('time', '')
    pz = get_current_timezone()
    if not time:
        errors['time'] = u"Дата та час завдання є обов'язковою"
    else:
        try:
            naive_time = datetime.strptime(time, '%Y-%m-%d %H:%M')
            new_task['time'] = pz.localize(naive_time)
        except ValueError:
            errors['time'] = u"Введіть коректний формат дати та часу"

    detail = request_info.get('detail', '')
    if not detail:
        errors['detail'] = u"Деталізація завдання є обов'язковою"
    else:
        new_task['detail'] = detail

    report = request_info.get('report', '')
    if report:
        try:
            new_task['report'] = Report.objects.get(pk=report)
        except:
            errors['report'] = "Такого провадження не існує"

    event = request_info.get('event', '')
    if event:
        try:
            new_task['event'] = ReportEvents.objects.get(pk=event)
            new_task['report'] = new_task['event'].report
        except:
            errors['event'] = "Будь-ласка, не втручайтесь в роботу сервісу!"

    return {'new_task': new_task, 'errors': errors}

def valid_detail_task(detail):
    new_task = {}
    valid = False
    report = detail.report
    date = datetime.strptime(detail.date, '%Y-%m-%d')
    if detail.name == 'schedule':
        subject = ReportSubject.objects.filter(report=report)[0]
        new_task['kind'] = u"Виїзд за адресою {}".format(subject.short_address())
        new_task['time'] = detail.time
        full_description = u"Огляд об'єкту {subject} за адресою {address}. {detail}".format(
            subject=subject.subject_type, address=subject.full_address(), detail=detail.info)
        new_task['detail'] = full_description
        new_task['report'] = detail.report
        new_task['event'] = detail
        valid = True

    elif detail.name == 'petition':
        new_task['kind'] = u"Направлення повідомлення про неможливість надання висновку"
        new_task['time'] = date + timedelta(days=90, hours=10)
        new_task['detail'] = u"Після направлення клопотання {} від {}".format(
            detail.subspecies, detail.date)
        new_task['report'] = detail.report
        new_task['event'] = detail
        valid = True

    elif detail.name == 'bill':
        new_task['kind'] = u'Відправлення без виконання (без оплати)'
        new_task['time'] = date + timedelta(days=45, hours=10)
        new_task['detail'] = u"{} від {}".format(detail.detail_info(), date.strftime("%Y-%m-%d"))
        new_task['report'] = detail.report
        new_task['event'] = detail
        valid = True

    return {'task_data': new_task, 'valid': valid} 