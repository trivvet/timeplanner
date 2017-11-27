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
def judges_list(request):
    judges = Judge.objects.all().order_by('surname')
    for judge in judges:
        judge.cases_amount = Report.objects.filter(judge_name=judge).count()
    header = 'Список суддів'
    return render(request, 'freports/judges_list.html', {'judges': judges, 'header': header})

@login_required(login_url='/login/')
def judge_detail(request, jid):
    judge = Judge.objects.get(pk=jid)
    cases = Report.objects.filter(judge_name=judge)
    next_url = request.GET.get('next')
    header = u'Детальна інформація про суддю {}'.format(judge.full_name())
    return render(request, 'freports/judge_detail.html', {'content': judge, 'header': header, 'cases': cases,
        'next_url': next_url})

@login_required(login_url='/login/')
def add_judge(request):
    header = u'Додавання судді'
    courts = Court.objects.all()
    if request.method == 'POST':
        if request.POST.get('cancel_next'):
            next_url = reverse(request.POST.get('cancel_next'), args=[request.POST.get('next_id')])
        else:
            next_url = reverse('judges_list')
        if request.POST.get('save_button'):
            valid_data = valid_judge(request.POST)
            errors = valid_data['errors']
            new_judge = valid_data['judge']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/judge_form.html',
                    {'content': new_judge, 'errors': errors, 'header': header, 'courts': courts})
            else:
                new_item = Judge(**new_judge)
                new_item.save()
                messages.success(request, u"Суддя %s успішно доданий" % new_item.short_name())
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання судді скасовано")

        return HttpResponseRedirect(next_url)

    else:
        next_url = request.GET.get('next', '')
        court_id = request.GET.get('court', '')
        content = {}
        if court_id:
            content['court_name'] = Court.objects.get(pk=court_id)
        return render(request, 'freports/judge_form.html', {'header': header, 'courts': courts, 'content': content,
            'cancel_url': next_url})

@login_required(login_url='/login/')
def edit_judge(request, jid):
    judge = Judge.objects.get(pk=jid)
    courts = Court.objects.all()
    header = u"Редагування інформацію про суддю {}".format(judge.short_name())
    if request.method == 'POST':
        if request.POST.get('cancel_next'):
            next_url = reverse(request.POST.get('cancel_next'), args=[jid])
        else:
            next_url = reverse('judges_list')
        if request.POST.get('save_button'):
            valid_data = valid_judge(request.POST)
            errors = valid_data['errors']
            edit_judge = valid_data['judge']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/judge_form.html',
                    {'content': edit_judge, 'errors': errors, 'header': header, 'courts': courts})
            else:
                edit_item = Judge(**edit_judge)
                edit_item.id = jid
                edit_item.save()
                messages.success(request, u"Інформація про суддю {} успішно змінена".format(edit_item.short_name()))
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування інформації про суддю скасовано")

        return HttpResponseRedirect(next_url)
    else:
        next_url = request.GET.get('next')
        return render(request, 'freports/judge_form.html', {'header': header, 'courts': courts, 'content': judge,
            'cancel_url': next_url})

@login_required(login_url='/login/')
def delete_judge(request, jid):
    judge = Judge.objects.get(pk=jid)
    header = u"Видалення інформації про суддю %s" % judge.short_name()
    content = u"Ви дійсно бажаєте видалити інформацію про суддю %s" % judge
    if request.method == "GET":
        next_url = request.GET.get('next')
        return render(request, 'freports/delete_form.html', {'content': content, 'header': header, 'cancel_url': next_url})
    else:
        next_url = reverse('judges_list')
        if request.POST.get('cancel_button'):
            if request.POST.get('cancel_next'):
                next_url = reverse(request.POST.get('cancel_next'), args=[jid])
            messages.warning(request, u"Видалення судді {} скасовано".format(judge.short_name()))
        elif request.POST.get('delete_button'):
            judge.delete()
            messages.success(request, u"Інформація про суддю %s успішно видалена" % judge)

        return HttpResponseRedirect(next_url)


def valid_judge(request_info):
    errors, new_judge = {}, {}

    surname = request_info['surname']
    if not surname:
        errors['surname'] = u"Прізвище судді є обов'язковим"
    else:
        new_judge['surname'] = surname

    first_name = request_info['first_name']
    if not first_name:
        errors['first_name'] = u"Ім'я судді є обов'язковим"
    else:
        new_judge['first_name'] = first_name

    second_name = request_info['second_name']
    if not second_name:
        errors['second_name'] = u"Ім'я по батькові судді є обов'язковим"
    else:
        new_judge['second_name'] = second_name

    court = request_info.get('court')
    if court:
        try:
            new_judge['court_name'] = Court.objects.get(pk=court)
        except ObjectDoesNotExist:
            errors['court'] = u"Будь ласка, виберіть суд зі списку"
    else:
        errors['court'] = u"Вибір суду є обов'язковим"

    new_judge['personal_phone'] = request_info['personal_phone']
    new_judge['work_phone'] = request_info['work_phone']
    new_judge['address'] = request_info['address']

    return {'judge': new_judge, 'errors': errors}
