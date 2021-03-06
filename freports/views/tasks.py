# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pytz, datetime
from datetime import date, datetime, timedelta
from calendar import day_abbr

from django.contrib import messages
from django.contrib.auth.decorators import (
    login_required, 
    permission_required
    )
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation, timezone
from django.utils.timezone import get_current_timezone, localtime, make_aware
from django.utils.formats import date_format

from ..models import Task, Report, ReportEvents, ReportSubject

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def tasks_list(request):
    all_tasks = Task.objects.all()
    content = {}
    content['active_tasks'] = all_tasks.exclude(execute=True).count()
    content['done_tasks'] = all_tasks.filter(execute=True).count()
    if request.GET.get('status'):
        tasks = all_tasks.filter(execute=True).order_by('time').reverse()
        if request.GET.get('all_pages', '') == '':
            paginator = Paginator(tasks, 15)
            page = request.GET.get('page', '')
            try:
                tasks = paginator.page(page)
            except PageNotAnInteger:
                tasks = paginator.page(1)
            except EmptyPage:
                tasks = paginator.page(paginator.num_pages)
    else:
        tasks = all_tasks.all().exclude(execute=True).order_by('time')        
    header = u'Список завдань'
    pz = get_current_timezone()
    return render(request, 'freports/tasks_list.html', 
    	{'tasks': tasks, 'header': header, 'today': pz.localize(datetime.now()),
        'content': content})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def change_status_task(request):
    if request.is_ajax():
        if request.method == "POST":
            try:
                executed_task = Task.objects.get(pk=request.POST.get('pk'))
            except:
                return JsonResponse({'status': 'error', 
                    'message': u"We can't find this task"})
            executed_task.execute = True
            executed_task.save()
            if executed_task.event and executed_task.event.name == 'schedule':
                next_url = reverse('freports:add_detail', 
                    kwargs={
                        'rid': executed_task.report.id, 
                        'kind': 'inspected'
                    })
            else:
                next_url = ''
            return JsonResponse({
                'status': 'success', 
                'next_url': next_url
            })
        else:
            try:
                executed_task = Task.objects.get(pk=request.GET.get('pk'))
            except:
                return JsonResponse({'status': 'error', 
                    'message': u"We can't find this task"})
            executed_task.execute = True
            executed_task.save()
            if executed_task.event and executed_task.event.name == 'schedule':
                return HttpResponseRedirect(reverse('report_add_detail', 
                    kwargs={'rid': executed_task.report.id, 'kind': 'inspected'}))
            report_id = request.GET.get('report')
            return JsonResponse({
                'status': 'success', 
                'modal': 'false'
            })

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def tasks_today_list(request):
    today = date.today()
    tasks = Task.objects.filter(time__startswith=today)
    tasks = tasks.exclude(execute=True).order_by('time')
    translation.activate('uk')
    header = u'{} {}'.format(date_format(today, 'l'), today.strftime("%d-%m-%Y"))
    return render(request, 'freports/tasks_today_list.html',
        {'tasks': tasks, 'header': header})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def add_task(request):
    header = u'Додавання завдання'
    reports = Report.objects.filter(executed=False).order_by('number')
    if request.method == 'POST':
        if request.POST.get('save_button'):
            valid_data = valid_task(request.POST)
            errors = valid_data['errors']
            new_task = valid_data['new_task']
            if errors:
                try:
                    new_task['time'] = localtime(new_task['time']).isoformat()
                except: 
                    pass
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/task_form.html', 
                    {'content': new_task, 'errors': errors, 'header': header, 'reports': reports})
            else:
                new_item = Task(**new_task)
                new_item.save()
                messages.success(request, u"Завдання %s успішно додане" % new_item)
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання завдання скасовано")
        next_page = request.POST.get('next_url', '')
        if next_page:
            url = next_page
        else:
            url = reverse('freports:tasks_list')
        return HttpResponseRedirect(url)

    else:
        next_page = request.GET.get('next_page', '')
        report_number = request.GET.get('report')
        if report_number:
            report = Report.objects.get(pk=report_number)
        else: 
            report = ''
        return render(request, 'freports/task_form.html', 
            {'header': header, 'reports': reports, 'next_url': next_page,
            'report_instance': report})

def add_detail_task(detail):
    new_task = valid_detail_task(detail)
    if new_task['valid']:
        new_item = Task(**new_task['task_data'])
        new_item.save()
    return HttpResponseRedirect(reverse('freports:tasks_list'))

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def edit_task(request, tid):
    task = Task.objects.get(pk=tid)
    header = u'Редагування інформації про завдання {name} яке призначене на {date}'.format(
        name=task.kind, date=task.time.strftime("%Y-%m-%d"))
    reports = Report.objects.filter(executed=False).order_by('number')
    report_instance = task.report
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
        
        next_page = request.POST.get('next_url', '')
        if next_page:
            url = next_page
        else:
            url = "%s?status=%s" % (reverse('freports:tasks_list'), 
                task.execute or '')
        return HttpResponseRedirect(url)
    else:
        task.time = localtime(task.time).isoformat()
        next_page = request.GET.get('next_page', '')
        return render(request, 'freports/task_form.html', 
            {'header': header, 'content': task, 'reports': reports,
                'next_url': next_page, 'report_instance': report_instance})

def edit_detail_task(detail):
    edit_task = Task.objects.filter(event=detail)
    new_task = valid_detail_task(detail)
    if new_task['valid']:
        new_item = Task(**new_task['task_data'])
        if edit_task:
            new_item.id = edit_task[0].id
        new_item.save()
    return HttpResponseRedirect(reverse('freports:tasks_list'))

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def delete_task(request, tid):
    next_page= request.GET.get('next_page', reverse('freports:tasks_list'))
    task = Task.objects.get(pk=tid)
    if request.method == 'POST':
        if request.POST.get('delete_button'):
            task.delete()
            messages.success(request, u"Завдання успішно видалене")
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання завдання скасовано")
        return HttpResponseRedirect(next_page)
    else:
        header = u'Видалення завдання'
        content = u"Ви дійсно бажаєте видалити інформацію про завдання {name} яке призначене на {date}?".format(
            name=task.kind, date=task.time.strftime("%Y-%m-%d"))
        return render(request, 'freports/delete_form.html', 
            {'content': content, 'header': header})

@login_required(login_url='/login/')
@permission_required('admins', raise_exception=True)
def delete_old_tasks(request):
    tasks = Task.objects.filter(execute=True)
    for task in tasks:
        substract = timezone.now().date() - task.time.date()
        if substract.days > 31:
            task.delete()
    messages.success(request, u"Завдання, виконані більше місяця тому, успішно видалено")
    return HttpResponseRedirect(reverse('freports:tasks_list'))

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

    execute = request_info.get('execute', '')

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
        new_task['time'] = date + timedelta(days=92, hours=10)
        new_task['detail'] = u"Після направлення клопотання {} від {}".format(
            detail.subspecies, date.strftime("%d-%m-%Y"))
        new_task['report'] = detail.report
        new_task['event'] = detail
        valid = True

    elif detail.name == 'bill':
        new_task['kind'] = u'Відправлення без виконання (без оплати)'
        task_time = date + timedelta(days=47, hours=10)
        new_task['time'] = make_aware(task_time)
        new_task['detail'] = u"{} від {}".format(detail.detail_info(), date.strftime("%d-%m-%Y"))
        new_task['report'] = detail.report
        new_task['event'] = detail
        valid = True

    return {'task_data': new_task, 'valid': valid} 