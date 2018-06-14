# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Report, ReportSubject

@login_required(login_url='/login/')
def subjects_list(request):
    all_subjects = ReportSubject.objects.all()
    paginator = Paginator(all_subjects, 10)
    page = request.GET.get('page', '')
    try:
        subjects = paginator.page(page)
    except PageNotAnInteger:
        subjects = paginator.page(1)
    except EmptyPage:
        subjects = paginator.page(paginator.num_page)
    header = u"Список об'єктів дослідження"
    return render(request, 'freports/subjects_list.html', {'subjects': subjects, 'header': header})

@login_required(login_url='/login/')
def subject_detail(request, sid):
    subject = ReportSubject.objects.get(pk=sid)
    header = u"Детальна інформація про об'єкт '%s' провадження №%s/%s" % (
        subject.subject_type, subject.report.number, subject.report.number_year)
    return render(request, 'freports/subject_detail.html', {'content': subject, 'header': header})

@login_required(login_url='/login/')
def add_subject(request, rid):
    report = Report.objects.get(pk=rid)
    subject = u'житловий будинок'
    header = u"Додавання об'єкту дослідження до провадження №%s/%s" % (report.number, report.number_year)

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_element = valid_data['data']

            if errors:
                new_element['settlement_type'] = request.POST.get('settlement_type')[0:2]
                new_element['settlement_name'] = request.POST.get('settlement_name')
                new_element['street_type'] = request.POST.get('street_type')[0:4]
                new_element['street_name'] = request.POST.get('street_name')
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/subject_form.html',
                    {'header': header, 'new_content': new_element, 'errors': errors})
            else:
                new_subject = ReportSubject(**new_element)
                new_subject.save()
                report = edit_report(new_subject, report)
                report.save()
                messages.success(request, u"Об'єкт '%s' успішно доданий" % new_subject.subject_type)

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання об'єкту до провадження скасовано")

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

    else:
        return render(request, 'freports/subject_form.html', {'header': header})

@login_required(login_url='/login/')
def edit_subject(request, rid, sid):
    report = Report.objects.get(pk=rid)
    subject = ReportSubject.objects.get(pk=sid)
    header = u"Редагування об'єкту '%s' провадження №%s/%s" % (subject.subject_type, report.number, report.number_year)

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_data = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                new_data['settlement_type'] = request.POST.get('settlement_type')[0:2]
                new_data['settlement_name'] = request.POST.get('settlement_name')
                new_data['street_type'] = request.POST.get('street_type')[0:4]
                new_data['street_name'] = request.POST.get('street_name')
                return render(request, 'freports/subject_form.html', {'new_content': new_data, 'errors': errors, 'header': header})

            else:
                edit_subject = ReportSubject(**new_data)
                edit_subject.id = sid
                edit_subject.save()
                report = edit_report(edit_subject, report)
                report.save()
                messages.success(request, u"Об'єкт '%s' успішно змінений" % edit_subject.subject_type)

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування об'єкту '%s' провадження №%s/%s  скасоване" %
                (subject.subject_type, report.number, report.number_year))

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

    else:
        return render(request, 'freports/subject_form.html', {'new_content': subject, 'header': header})

@login_required(login_url='/login/')
def delete_subject(request, rid, sid):
    report = Report.objects.get(pk=rid)
    subject = ReportSubject.objects.get(pk=sid)
    content = u"Ви дійсно бажаєте видалити об'єкт '%s' провадження №%s/%s, що знаходиться за адресою %s?" % (
        subject.subject_type, report.number, report.number_year, subject.full_address())
    header = u"Видалення об'єкту '%s' провадження №%s/%s" % (subject.subject_type, report.number, report.number_year)

    if request.method == 'GET':
        return render(request, 'freports/delete_form.html', {'report': report, 'content': content, 'header': header})

    elif request.method == 'POST':
        if request.POST.get('delete_button'):
            subject_delete = subject
            subject_delete.delete()
            report = edit_report(False, report)
            report.save()
            messages.success(request, u"Об'єкт '%s' провадження №%s/%s успішно видалений" % (
                subject.subject_type, report.number, report.number_year))
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення об'єкту '%s' провадження №%s/%s скасоване" % (
                subject.subject_type, report.number, report.number_year))

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

def valid_detail(request_info, report_id):
    errors = {}
    new_element = {}

    new_element['report'] = Report.objects.get(id=report_id)

    subject_type = request_info.get('subject_type')
    if not subject_type:
        errors['subject_type'] = u"Інформація про вид об'єкту дослідження є обов'язковою"
    else:
        new_element['subject_type'] = subject_type

    settlement = request_info.get('settlement_name')
    settlement_type = request_info.get('settlement_type')
    if not settlement:
        errors['settlement'] = u"Назва населеного пункту є обов'язковою"
    else:
        if settlement_type:
            new_element['settlement'] = u"%s %s" % (settlement_type, settlement)
        else:
            new_element['settlement'] = settlement

    region = request_info.get('region')
    new_element['region'] = region

    street_name = request_info.get('street_name')
    street_type = request_info.get('street_type')
    if not street_name:
        errors['street'] = u"Назва вулиці є обов'язковою"
    else:
        if street_type:
            new_element['street'] = u"%s %s" % (street_type, street_name)
        else:
            new_element['street'] = street_name

    building = request_info.get('building')
    new_element['building'] = building

    flat = request_info.get('flat')
    new_element['flat'] = flat

    research_type = request_info.get('research_type')
    if not research_type:
        errors['research_type'] = u"Інформація про тип дослідження є обов'язковою"
    else:
        new_element['research_type'] = research_type

    return {'errors': errors, 'data': new_element}

def object_name_replace(report_subject_name, subject_name):
    replace_dict = {
        'земельна ділянка': 'земельні ділянки',
        'квартира': 'квартири',
        'житловий будинок': 'житлові будинки',
        'нежитлове приміщення': 'нежитлові приміщення',
        'гараж': 'гаражі'
    }
    report_subject_name = report_subject_name.replace(subject_name, replace_dict[subject_name])
    return report_subject_name

def edit_report(subject, report):
    report_subjects = ReportSubject.objects.filter(report=report)
    if subject is False and report_subjects.count() != 0:
        pass
    elif subject is False:
        report.address = '-'
        report.object_name = '-'
        report.research_kind = '-'
    else:
        if report_subjects.count() > 1:
            if subject.subject_type not in report.object_name:
                report.object_name = "{}, {}".format(report.object_name, subject.subject_type)
            else:
                report.object_name = object_name_replace(report.object_name, subject.subject_type)
            report.address == "{}, {}".format(report.address, subject.short_address())
            if subject.research_type not in report.research_kind:
                report.research_kind = "{}, {}".format(report.research_kind, subject.research_type)
        else:
            report.address = subject.short_address()
            report.object_name = subject.subject_type
            report.research_kind = subject.research_type

    return report
