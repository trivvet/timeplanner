# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from ..models import Court, Judge, Report

@login_required(login_url='/login/')
def courts_list(request):
    courts = Court.objects.all().order_by('name')
    for court in courts:
        judges = Judge.objects.filter(court_name=court)
        court.cases_amount = 0
        court.executed_amount = 0
        for judge in judges:
            court.cases_amount += Report.objects.filter(judge_name=judge, executed=False).count()
            court.executed_amount += Report.objects.filter(judge_name=judge, executed=True).count()
    header = 'Список судів'
    return render(request, 'freports/courts_list.html', 
        {'courts': courts, 'header': header})

@login_required(login_url='/login/')
def court_detail(request, cid):
    court = Court.objects.get(pk=cid)
    judges = Judge.objects.filter(court_name=court)
    cases_amount = 0
    for judge in judges:
        cases_amount += Report.objects.filter(judge_name=judge, executed=False).count()
    header = u'Детальна інформація про {}'.format(court.name)
    return render(request, 'freports/court_detail.html', 
        {'content': court, 'header': header, 'judges': judges,
         'cases_amount': cases_amount})

@login_required(login_url='/login/')
def add_court(request):
    header = u'Додавання суду'
    if request.method == 'POST':
        if request.POST.get('save_button'):
            valid_data = valid_court(request.POST)
            errors = valid_data['errors']
            new_court = valid_data['new_court']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/court_form.html', 
                    {'content': new_court, 'errors': errors, 
                     'header': header})
            else:
                new_item = Court(**new_court)
                new_item.save()
                messages.success(request, u"%s успішно доданий" % new_item)
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання суду скасовано")

        return HttpResponseRedirect(reverse('freports:courts_list'))

    else:
        return render(request, 'freports/court_form.html', 
            {'header': header})

@login_required(login_url='/login/')
def edit_court(request, cid):
    court = Court.objects.get(pk=cid)
    header = u'Редагування інформації про {}'.format(court.name)
    judges = Judge.objects.filter(court_name=court)
    if request.method == 'POST':
        next_url = request.POST.get('next_url', '')
        if request.POST.get('save_button'):
            valid_data = valid_court(request.POST)
            errors = valid_data['errors']
            new_court = valid_data['new_court']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/court_form.html', {'content': new_court, 'errors': errors, 'header': header,
                    'judges': judges, 'next_url': next_url})
            else:
                new_item = Court(**new_court)
                new_item.id=cid
                new_item.save()
                messages.success(request, u"Інформація про %s успішно змінена" % new_item)
        elif request.POST.get('cancel_button'):
            messages.warning(request, 
                u"Редагування інформації про {} скасовано".format(court.name))
        if next_url == '':
            next_url = reverse('freports:courts_list')

        return HttpResponseRedirect(next_url)

    else:
        next_url_name, next_url = request.GET.get('next', ''), ''
        if next_url_name:
            next_url = reverse(next_url_name, args=[cid])
        return render(request, 'freports/court_form.html', 
            {'header': header, 'content': court, 'judges': judges,
             'next_url':next_url})

@login_required(login_url='/login/')
def delete_court(request, cid):
    court = Court.objects.get(pk=cid)
    header = u"Видалення інформації про %s" % court
    content = u"Ви дійсно бажаєте видалити інформацію про {}?".format(court.name)
    if request.method == "GET":
        next_url_name, next_url = request.GET.get('next', ''), ''
        if next_url_name:
            next_url = reverse(next_url_name, args=[cid])
        return render(request, 'freports/delete_form.html', 
            {'content': content, 'header': header, 
             'cancel_url': next_url})
    else:
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення інформації про {} скасовано".format(court.name))
            next_url = request.POST.get('cancel_next')
        elif request.POST.get('delete_button'):
            judges = Judge.objects.filter(court_name=court)
            if judges.count() > 0:
                messages.error(request, u"Видалення неможливе. У складі даного суду наявні судді!")
                next_url = request.POST.get('cancel_next')
            else:
                next_url = ''
                court.delete()
                messages.success(request, u"%s успішно видалений" % court)

        if next_url:
            return HttpResponseRedirect(next_url)
        else:
            return HttpResponseRedirect(reverse('freports:courts_list'))


def valid_court(request_info):
    errors, new_court = {}, {}
    name = request_info['name']
    if not name:
        errors['name'] = u"Назва суду є обов'язковою"
    else:
        new_court['name'] = name

    number = request_info['number']
    try:
        new_court['number'] = int(number)
    except ValueError:
        new_court['number'] = None

    new_court['address'] = request_info['address']

    chair = request_info.get('chair')
    if chair:
        try:
            new_court['chair'] = Judge.objects.get(pk=chair)
        except ObjectDoesNotExist:
            errors['chair'] = u"Будь ласка, виберіть суддю зі списку"

    return {'new_court': new_court, 'errors': errors}
