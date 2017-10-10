# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from .models import ForensicReport

def reports_list(request):
    reports = ForensicReport.objects.all()
    return render(request, 'freports/reports_list.html', {'reports': reports})

def add_report(request):
    header = 'Додавання провадження'

    if request.method == 'POST':
        errors = {}
        if request.POST.get('save_button'):

            report_number = request.POST.get('number')
            if not report_number:
                errors['number'] = '1'

            address = request.POST.get('address')
            if not address:
                errors['address'] = '1'

            plaintiff = request.POST.get('plaintiff')
            if not plaintiff:
                errors['plaintiff'] = '1'

            defendant = request.POST.get('defendant')
            if not defendant:
                errors['defendant'] = '1'

            object_name = request.POST.get('object_name')
            if not object_name:
                errors['object_name'] = '1'

            research_kind = request.POST.get('research_kind')
            if not research_kind:
                errors['research_kind'] = '1'

            if errors:
                messages.error(request, "Виправте наступні недоліки")
                return render(request, 'freports/add_report.html', {'header': header})

            else:
                new_report = ForensicReport(number=report_number, address=address, plaintiff=plaintiff, defendant=defendant,
                    object_name=object_name, research_kind=research_kind)
                new_report.save()
                messages.success(request, "Провадження №%s успішно додане" % report_number)

        elif request.POST.get('cancel_button'):
            messages.warning(request, "Додавання провадження скасовано")

        return HttpResponseRedirect(reverse('forensic_reports_list'))

    else:
        return render(request, 'freports/add_report.html', {'header': header})


def edit_report(request, rid):
    header = 'Редагування провадження'
    content = ForensicReport.objects.get(pk=rid)

    if request.method == 'POST':
        errors = {}
        if request.POST.get('save_button'):

            report_number = request.POST.get('number')
            if not report_number:
                errors['number'] = '1'

            address = request.POST.get('address')
            if not address:
                errors['address'] = '1'

            plaintiff = request.POST.get('plaintiff')
            if not plaintiff:
                errors['plaintiff'] = '1'

            defendant = request.POST.get('defendant')
            if not defendant:
                errors['defendant'] = '1'

            object_name = request.POST.get('object_name')
            if not object_name:
                errors['object_name'] = '1'

            research_kind = request.POST.get('research_kind')
            if not research_kind:
                errors['research_kind'] = '1'

            current_report = content
            current_report.number=report_number
            current_report.address=address
            current_report.plaintiff=plaintiff
            current_report.defendant=defendant
            current_report.object_name=object_name
            current_report.research_kind=research_kind

            if errors:
                messages.success(request, "Виправте наступні недоліки")
                return render(request, 'freports/add_report.html', {'header': header, 'content': content})

            else:
                current_report.save()
                messages.success(request, "Провадження №%s успішно відкориговане" % report_number)

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


