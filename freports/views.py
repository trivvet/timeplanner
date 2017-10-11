# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import ForensicReport

def reports_list(request):
    reports = ForensicReport.objects.all().order_by('number')
    order_by = request.GET.get('order_by')
    if order_by:
        reports = reports.order_by(order_by)
    return render(request, 'freports/reports_list.html', {'reports': reports})

def add_report(request):
    header = u'Додавання провадження'

    if request.method == 'POST':
        if request.POST.get('save_button'):
            validate_data = valid_report(request.POST)
            errors = validate_data['errors']
            new_report = validate_data['data_report']

            if errors:
                messages.error(request, "Виправте наступні недоліки")
                return render(request, 'freports/add_report.html', {'header': header, 'errors': errors,
                    'content': new_report})

            else:
                new_report = ForensicReport(**new_report)
                new_report.save()
                messages.success(request, "Провадження №%s/017 успішно додане" % new_report.number)

        elif request.POST.get('cancel_button'):
            messages.warning(request, "Додавання провадження скасовано")

        return HttpResponseRedirect(reverse('forensic_reports_list'))

    else:
        return render(request, 'freports/add_report.html', {'header': header})


def edit_report(request, rid):
    header = 'Редагування провадження'
    content = ForensicReport.objects.get(pk=rid)

    if request.method == 'POST':
        if request.POST.get('save_button'):
            current_report = content

            validate_data = valid_report(request.POST)
            errors = validate_data['errors']
            new_report = validate_data['data_report']

            if errors:
                messages.error(request, "Виправте наступні недоліки")
                return render(request, 'freports/add_report.html', {'header': header, 'content': new_report,
                    'errors': errors})

            else:
                current_report.number = new_report['number']
                current_report.address = new_report['address']
                current_report.plaintiff = new_report['plaintiff']
                current_report.defendant = new_report['defendant']
                current_report.object_name = new_report['object_name']
                current_report.research_kind = new_report['research_kind']
                current_report.save()
                messages.success(request, "Провадження №%s/017 успішно відкориговане" % current_report.number)

        elif request.POST.get('cancel_button'):
            messages.warning(request, "Редагування провадження скасовано")

        return HttpResponseRedirect(reverse('forensic_reports_list'))

    else:
        return render(request, 'freports/add_report.html', {'header': header, 'content': content})


def delete_report(request, rid):
    if request.method == 'GET':
        report = ForensicReport.objects.get(pk=rid)
        return render(request, 'freports/delete_report.html', {'report': report})
    elif request.method == 'POST':
        if request.POST.get('delete_button'):
            current_report = ForensicReport.objects.get(pk=rid)
            current_report.delete()
            messages.success(request, "Провадження №%s успішно видалено" % current_report.number)
        elif request.POST.get('cancel_button'):
            messages.warning(request, "Видалення провадження скасовано")

        return HttpResponseRedirect(reverse('forensic_reports_list'))

def valid_report(data_post):
    errors = {}
    new_report = {}

    report_number = data_post.get('number')
    if not report_number:
        errors['number'] = u"Номер висновку є обов'язковим"
    else:
        try:
            new_report['number'] = int(report_number)
        except ValueError:
            new_report['number'] = report_number
            errors['number'] = u"Будь-ласка введіть число"

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


