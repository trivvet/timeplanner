# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from ..models import Report, ReportEvents, ReportParticipants, Contacts

status_list = {
    'judge': 'Суддя',
    'plaintiff': 'Позивач',
    'defendant': 'Відповідач',
    'plaintiff_agent': 'Представник позивача',
    'defendant_agent': 'Представник відповідача',
    'other_participant': 'Інший учасник'}

@login_required(login_url='/login/')
def participants_list(request):
    all_participants = ReportParticipants.objects.all()
    for participant in all_participants:
        participant.status = status_list[participant.status]
    paginator = Paginator(all_participants, 10)
    page = request.GET.get('page', '')
    try:
        participants = paginator.page(page)
    except PageNotAnInteger:
        participants = paginator.page(1)
    except EmptyPage:
        participants = paginator.page(paginator.num_page)
    header = u'Список учасників проваджень'
    return render(request, 'freports/participants_list.html', {'participants': participants, 'header': header})

@login_required(login_url='/login/')
def participant_detail(request, rid):
    participant = ReportParticipants.objects.get(pk=rid)
    participant.status = status_list[participant.status]
    header = u'Детальна інформація про учасника провадження №%s/%s' % (participant.report.number, participant.report.number_year)
    return render(request, 'freports/participant_detail.html', {'content': participant, 'header': header})

@login_required(login_url='/login/')
def add_participant(request, rid, status):
    report = Report.objects.get(pk=rid)
    header = u'Додавання учасника "%s" до провадження №%s/%s' % (status_list[status], report.number, report.number_year)

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid, status)
            errors = valid_data['errors']
            new_element = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/participant_form.html',
                    {'content': new_element, 'errors': errors, 'header': header, 'status': status})

            else:
                new_participant = ReportParticipants(**new_element)
                new_participant.save()
                updated_contact = find_contact(new_participant)
                if updated_contact:
                    updated_contact.save()
                report = edit_report(new_participant, report)
                report.save()
                messages.success(request, u"%s '%s' успішно доданий" % (status_list[new_participant.status], new_participant.surname))

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання учасника провадження скасовано")

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

    else:
        return render(request, 'freports/participant_form.html', {'header': header, 'status': status})

@login_required(login_url='/login/')
def edit_participant(request, rid, did):
    report = Report.objects.get(pk=rid)
    participant = ReportParticipants.objects.get(pk=did)
    header = u"Редагування учасника '%s %s' провадження №%s/%s" % (
        status_list[participant.status], participant.surname, report.number, report.number_year)

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid, participant.status)
            errors = valid_data['errors']
            new_data = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/participant_form.html', {'content': new_data, 'errors': errors})

            else:
                edit_participant = ReportParticipants(**new_data)
                edit_participant.id = participant.id
                edit_participant.save()
                updated_contact = find_contact(edit_participant)
                if updated_contact:
                    updated_contact.save()
                report = edit_report(edit_participant, report)
                report.save()
                messages.success(request, u"%s '%s' успішно змінений" % (
                    status_list[edit_participant.status], edit_participant.surname))

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування учасника провадження №%s/%s '%s %s' скасоване" %
                (report.number, report.number_year, status_list[participant.status], participant.surname))

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

    else:
        content = participant
        return render(request, 'freports/participant_form.html', {'content': content, 'header': header})

@login_required(login_url='/login/')
def delete_participant(request, rid, did):
    report = Report.objects.get(pk=rid)
    participant = ReportParticipants.objects.get(pk=did)
    content = u"Ви дійсно бажаєте видалити '%s %s' провадження №%s/%s?" % (
        status_list[participant.status], participant.surname, report.number, report.number_year)
    header = u"Видалення '%s %s' провадження №%s/%s" % (
        status_list[participant.status], participant.surname, report.number, report.number_year)

    if request.method == 'GET':
        return render(request, 'freports/delete_form.html', {'report': report, 'content': content, 'header': header})

    elif request.method == 'POST':
        if request.POST.get('delete_button'):
            participant_delete = participant
            participant_delete.delete()
            report = edit_report(participant_delete, report, 'delete')
            report.save()
            messages.success(request, u"%s '%s' провадження №%s/%s успішно видалений" % (
                status_list[participant.status], participant.surname, report.number, report.number_year))
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення учасника провадження №%s/%s '%s %s' скасоване" % (
                report.number, report.number_year, status_list[participant.status], participant.surname))

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

def valid_detail(request_info, report_id, main_status):
    errors = {}
    new_element = {}

    report = Report.objects.filter(pk=report_id)
    if len(report) != 1:
        errors['report'] = u'На сервері сталася помилка. Будь-ласка спробуйте пізніше'
    else:
        new_element['report'] = report[0]

    surname = request_info.get('surname')
    if not surname:
        errors['surname'] = u"Прізвище учасника є обов'язковим"
    else:
        new_element['surname'] = surname

    if main_status != 'other_participant':
        new_element['status'] = main_status
    else:
        status = request_info.get('status')
        if not status:
            errors['status'] = u"Виберіть статус учасника"
        else:
            new_element['status'] = status

    new_element['name'] = request_info.get('name')
    new_element['address'] = request_info.get('address')
    new_element['phone'] = request_info.get('phone')
    new_element['info'] = request_info.get('info')

    return {'errors': errors, 'data': new_element}

def find_contact(participant):
    contact = False
    if participant.address or participant.phone:
        current_contacts = Contacts.objects.filter(surname=participant.surname)
        if current_contacts and current_contacts[0].status == participant.status:
            current_contact = current_contacts[0]
            if participant.name:
                if current_contact.name and current_contact.name != participant.name:
                    current_contact.name = current_contact.name + '; ' + participant.name
                else:
                    current_contact.name = participant.name
            if participant.address:
                if current_contact.address and current_contact.address != participant.address:
                    current_contact.address = current_contact.address + '; ' + participant.address
                else:
                    current_contact.address = participant.address
            if participant.phone:
                if current_contact.phone and current_contact.phone != participant.phone:
                    current_contact.phone = current_contact.phone + '; ' + participant.phone
                else:
                    current_contact.phone = participant.phone
            if participant.info:
                if current_contact.info and current_contact.info != participant.info:
                    current_contact.info = current_contact.info + '; ' + participant.info
                else:
                    current_contact.info = participant.info
            contact = current_contact

        else:
            contact = Contacts(surname=participant.surname, name=participant.name, status=participant.status,
                address=participant.address, phone=participant.phone, info=participant.info)

    return contact

def edit_report(participant, report, *args):
    participants = ReportParticipants.objects.filter(report=report)
    plaintiffs = participants.filter(report=report, status='plaintiff')
    defendants = participants.filter(report=report, status='defendant')
    if participant.status == 'plaintiff':
        if 'delete' in args and participant.surname in report.plaintiff:
            if plaintiffs.count() > 0:
                report.plaintiff = plaintiffs[0].surname
            else:
                report.plaintiff = '-'
        elif plaintiffs.count() == 0:
            report.plaintiff = '-'
        elif plaintiffs.count() == 1:
            report.plaintiff = plaintiffs[0].surname
    elif participant.status == 'defendant':
        if 'delete' in args and participant.surname in report.defendant:
            if defendants.count() > 0:
                report.defendant = defendants[0].surname
            else:
                report.defendant = '-'
        elif defendants.count() == 1:
            report.defendant = defendants[0].surname
    return report
