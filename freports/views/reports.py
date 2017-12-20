# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from itertools import chain
from datetime import date

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from .days_counter import days_amount
from ..models import Report, ReportEvents, Judge, Court, ReportParticipants, ReportSubject

@login_required(login_url='/login/')
def reports_list(request):
    content = {}
    days_count = ''


    if request.GET.get('executed'):
        reports = Report.objects.filter(executed=True)
        content['reports_count'] = reports.count()
    elif request.GET.get('deactivate'):
        reports = Report.objects.filter(executed=False, active=False)
        content['reports_count'] = reports.count()
    elif request.GET.get('activate'):
        reports = Report.objects.filter(executed=False, active=True)
        content['reports_count'] = reports.count()
    else:
        reports = Report.objects.all()
        content['open_reports'] = reports.filter(executed=False).count()
        content['closed_reports'] = reports.filter(executed=True).count()
        content['active_reports'] = reports.filter(executed=False, active=True).count()

    reports = reports.order_by('number')

    if request.GET.get('filter_status') and request.GET.get('apply_button'):

        date_from = request.GET.get('date_from')
        if date_from:
            reports = reports.filter(date_arrived__gt=date_from)

        date_until = request.GET.get('date_until')
        if date_until:
            reports = reports.filter(date_arrived__lt=date_until)

        days_count = request.GET.get('day_count')

    elif request.GET.get('filter_status') and request.GET.get('cancel_button'):
        return HttpResponseRedirect(reverse('forensic_reports_list'))

    order_by = request.GET.get('order_by', '')
    reverse_apply = request.GET.get('reverse', '')
    if order_by in ('research_kind', 'number'):
        reports = reports.order_by(order_by)
        if reverse_apply:
            reports = reports.reverse()
        reports_out = reports
    elif order_by == 'days_amount':
        reports_out = []
        for report in reports:
            if len(reports_out) > 0:
                index = 0
                for report_out in reports_out:
                    if report.active_days() < report_out.active_days():
                        reports_out.insert(index, report)
                        break
                    elif index < len(reports_out)-1:
                        index += 1
                    else:
                        reports_out.append(report)
            else:
                reports_out.append(report)
    else:
        reports_out = reports

    return render(request, 'freports/reports_list.html', {'reports': reports_out, 'content': content})

@login_required(login_url='/login/')
def add_new_report_first(request):
    header = u'Спочатку виберіть замовника дослідження'
    courts = Court.objects.all()
    for court in courts:
        court.judges = Judge.objects.filter(court_name=court)
    return render(request, 'freports/add_new_report_first.html', {'header': header, 'courts': courts})

@login_required(login_url='/login/')
def add_new_report(request):
    header = u'Зазначте номер нового провадження'

    if request.method == 'POST':
        judge_id = request.POST.get('judge_id', '')
        if request.POST.get('cancel_next'):
            next_url = reverse(request.POST.get('cancel_next'), args=[judge_id])
        else:
            next_url = reverse('forensic_reports_list')
        if request.POST.get('save_button'):
            data = request.POST
            errors, new_data = {}, {}

            if data['number']:
                try:
                    new_data['number'] = int(data['number'])
                except ValueError:
                    errors['number'] = u"Будь-ласка введіть ціле число"
                    new_data['number'] = data['number']
            else:
                errors['number'] = u"Номер висновку є обов'язковим"

            if errors:
                messages.error(request, "Виправте наступні недоліки")
                return render(request, 'freports/add_new_report.html', {'header': header, 'errors': errors,
                    'content': new_data, 'judge_id': judge_id})
            else:
                new_data['number_year'] = data['number_year']
                new_data['address'] = u"-"
                new_data['plaintiff'] = u"-"
                new_data['defendant'] = u"-"
                new_data['object_name'] = u"-"
                new_data['research_kind'] = u"-"
                new_data['active'] = None
                if judge_id:
                    new_data['judge_name'] = Judge.objects.get(pk=judge_id)
                new_report = Report(**new_data)
                new_report.save()

                messages.success(request, "Провадження №%s/%s успішно створене" % (
                    new_report.number, new_report.number_year))
        elif request.POST.get('cancel_button'):
            messages.warning(request, "Створення нового провадження скасовано")
        return HttpResponseRedirect(next_url)

    else:
        judge_id = request.GET.get('judge', '')
        next_url = request.GET.get('next', '')
        return render(request, 'freports/add_new_report.html', {'header': header, 'judge_id': judge_id,
            'cancel_url': next_url})

@login_required(login_url='/login/')
def edit_report(request, rid):
    header = 'Редагування провадження'
    content = Report.objects.get(pk=rid)
    courts = Court.objects.all()
    judges = Judge.objects.filter(court_name=content.judge_name.court_name)

    if request.method == 'POST':
        if request.POST.get('next'):
            next_url = reverse(request.POST.get('next'), args=[rid])
        else:
            next_url = reverse('forensic_reports_list')

        if request.POST.get('save_button'):

            validate_data = valid_report(request.POST)
            errors = validate_data['errors']
            new_report = validate_data['data_report']

            if errors:
                messages.error(request, "Виправте наступні недоліки")
                new_report['judge_name'] = content.judge_name
                return render(request, 'freports/add_report.html', {'header': header, 'content': new_report,
                    'errors': errors, 'courts': courts, 'judges': judges})

            else:
                current_report = Report(**new_report)
                current_report.id = rid
                current_report.active = content.active

                current_report.save()
                messages.success(request, u"Провадження №%s/%s успішно відкориговане" % (current_report.number, current_report.number_year))

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування провадження скасовано")

        return HttpResponseRedirect(next_url)

    else:
        if request.is_ajax():
            court = Court.objects.get(pk=request.GET.get('court'))
            judges = Judge.objects.filter(court_name=court)
            new_list = []
            for judge in judges:
                new_item = {'id': judge.id, 'short_name': judge.short_name()}
                new_list.append(new_item)
            return JsonResponse({'status': 'success', 'judges': new_list, 'court_number': court.number})
        else:
            content.date_arrived = content.date_arrived.isoformat()
            if content.executed:
                content.date_executed = content.date_executed.isoformat()
            next_url = request.GET.get('next', '')
            return render(request, 'freports/add_report.html', {'header': header, 'content': content, 'courts': courts,
                'judges': judges, 'next_url': next_url})

@login_required(login_url='/login/')
def delete_report(request, rid):
    if request.method == 'GET':
        report = Report.objects.get(pk=rid)
        content = u"Ви дійсно бажаєте видалите провадження №%s/017?" % report.number
        header = u"Видалення провадження №%s/017" % report.number
        return render(request, 'freports/delete_form.html', {'report': report, 'header': header, 'content': content})
    elif request.method == 'POST':
        if request.POST.get('delete_button'):
            current_report = Report.objects.get(pk=rid)
            participants = ReportParticipants.objects.filter(report=current_report)
            subjects = ReportSubject.objects.filter(report=current_report)
            if participants.count() > 0:
                messages.error(request, u"Видалення неможливе. За даним провадженням рахуються учасники справи!")
            elif subjects.count() > 0:
                messages.error(request, u"Видалення неможливе. За даним провадженням рахуються об'єкти дослідження!")
            else:
                current_report.delete()
                messages.success(request, u"Провадження №%s/017 успішно видалено" % current_report.number)
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення провадження скасовано")

        return HttpResponseRedirect(reverse('forensic_reports_list'))

def valid_report(data_post):
    errors = {}
    new_report = {}

    date_arrived = data_post.get('date_arrived')
    if not date_arrived:
        errors['date_arrived'] = u"Дата надходження є обов'язковою"
    else:
        try:
            new_report['date_arrived'] = date_arrived
        except ValueError:
            errors['date_arrived'] = u"Введіть коректний формат дати"

    report_number = data_post.get('number')
    if not report_number:
        errors['number'] = u"Номер висновку є обов'язковим"
    else:
        try:
            new_report['number'] = int(report_number)
        except ValueError:
            new_report['number'] = report_number
            errors['number'] = u"Будь-ласка введіть ціле число"

    new_report['number_year'] = data_post.get('number_year')

    judge_name = data_post.get('judge')
    if not judge_name:
        errors['judge'] = u"Вибір судді є обов'язковим"
    else:
        try:
            new_report['judge_name'] = Judge.objects.get(pk=judge_name)
        except ObjectDoesNotExist:
            errors['judge'] = u"Будь-ласка виберіть суддю зі списку"

    case_number = data_post.get('case_number')
    if not case_number:
        errors['case_number'] = u"Номер справи є обов'язковим"
    else:
        new_report['case_number'] = case_number

    address = data_post.get('address')
    if not address:
        errors['address'] = u"Адреса об'єкту є обов'язковою"
    else:
        new_report['address'] = address

    plaintiff = data_post.get('plaintiff')
    if not plaintiff:
        errors['plaintiff'] = u"Прізвище позивача є обов'язковим"
    else:
        new_report['plaintiff'] = plaintiff

    defendant = data_post.get('defendant')
    if not defendant:
        errors['defendant'] = u"Прізвище відповідача є обов'язковим"
    else:
        new_report['defendant'] = defendant

    object_name = data_post.get('object_name')
    if not object_name:
        errors['object_name'] = u"Тип об'єкту є обов'язковим"
    else:
        new_report['object_name'] = object_name

    research_kind = data_post.get('research_kind')
    if not research_kind:
        errors['research_kind'] = u"Вид дослідження є обов'язковим"
    else:
        new_report['research_kind'] = research_kind

    return {'errors': errors, 'data_report': new_report}
