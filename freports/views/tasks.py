# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz, datetime
from datetime import datetime

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.timezone import get_current_timezone, localtime

from ..models import Task

@login_required(login_url='/login/')
def tasks_list(request):
    tasks = Task.objects.all().order_by('time')
    header = 'Список завдань'
    return render(request, 'freports/tasks_list.html', 
    	{'tasks': tasks, 'header': header})


@login_required(login_url='/login/')
def add_task(request):
    header = u'Додавання завдання'
    if request.method == 'POST':
        if request.POST.get('save_button'):
            valid_data = valid_task(request.POST)
            errors = valid_data['errors']
            new_task = valid_data['new_task']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/task_form.html', 
                    {'content': new_task, 'errors': errors, 'header': header})
            else:
                new_item = Task(**new_task)
                new_item.save()
                messages.success(request, u"Завдання %s успішно додане" % new_item)
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання завдання скасовано")

        return HttpResponseRedirect(reverse('tasks_list'))

    else:
        return render(request, 'freports/task_form.html', {'header': header})

@login_required(login_url='/login/')
def edit_task(request, tid):
    task = Task.objects.get(pk=tid)
    header = u'Редагування інформації про завдання {name} яке призначене на {date}'.format(
        name=task.kind, date=task.time.strftime("%Y-%m-%d"))
    if request.method == 'POST':
        if request.POST.get('save_button'):
            valid_data = valid_task(request.POST)
            errors = valid_data['errors']
            edit_task = valid_data['new_task']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freposts/task_form.html',
                    {'content': edit_task, 'errors': errors, 'header': header})
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
            {'header': header, 'content': task})

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
    
    time = request_info.get('time')
    pz = get_current_timezone()
    if not time:
        errors['time'] = u"Дата та час завдання є обов'язковою"
    else:
        try:
            naive_time = datetime.strptime(time, '%Y-%m-%d %H:%M')
            new_task['time'] = pz.localize(naive_time)
        except ValueError:
            errors['time'] = u"Введіть коректний формат дати та часу"

    detail = request_info['detail']
    if not detail:
        errors['detail'] = u"Деталізація завдання є обов'язковою"
    else:
        new_task['detail'] = detail

    return {'new_task': new_task, 'errors': errors}