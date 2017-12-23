# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime, date

from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .days_counter import active_days, waiting_days
from ..models import Report, ReportEvents, ReportParticipants, ReportSubject, Court, Judge

petition_type = ['Про надання додаткових матеріалів', 'Про уточнення питань', 'Про надання справи', 'Про призначення виїзду']
done_type = ['Висновок експерта', 'Повідомлення про неможливість', 'Залишення без виконання']
inspected_type = ['Проведено успішно', 'Не надано доступ', 'Відмінено']
bill_type = ['Направлено рекомендованого листа', 'Вручено особисто', 'Вручено представнику', 'Направлено електронного листа']
paid_type = ['На банківський рахунок', 'Готівкою']
kind_specific = {
        'first_arrived': ['надходження ухвали', ['date', 'info', 'received', 'decision_date']],
        'arrived': ['надходження з суду', ['date', 'info', 'received']],
        'petition': ['направлення клопотання', ['date', 'info', 'type', 'necessary', 'sending'], petition_type],
        'bill': ['направлення рахунку', ['date', 'info', 'cost', 'address', 'type'], bill_type],
        'paid': ['оплата', ['date', 'info', 'type'], paid_type],
        'schedule': ['призначення виїзду', ['date', 'info', 'time']],
        'inspected': ['проведення огляду', ['date', 'info', 'type'], inspected_type],
        'done': ['відправлення до суду', ['date', 'info', 'sending', 'type'], done_type]}

status_list = {
    'judge': 'Суддя',
    'plaintiff': 'Позивач',
    'defendant': 'Відповідач',
    'plaintiff_agent': 'Представник позивача',
    'defendant_agent': 'Представник відповідача',
    'other_participant': 'Інший учасник'}

@login_required(login_url='/login/')
def details_list(request, rid):
    report = Report.objects.get(pk=rid)
    details = ReportEvents.objects.filter(report=report).order_by('date')

    if len(details.filter(name='first_arrived')) < 1:
        return HttpResponseRedirect(reverse('report_add_order', args=[rid]))

    report.last_event = details.reverse()[0]

    participants_list = ReportParticipants.objects.filter(report=report)
    participants = {'other': []}
    subjects = ReportSubject.objects.filter(report=report)
    for participant in participants_list:
        if participant.status in ['judge', 'plaintiff', 'defendant']:
            try:
                participants[participant.status]
            except KeyError:
                participants[participant.status] = []
            participants[participant.status].append(participant)
        else:
            participant.status = status_list[participant.status]
            participants['other'].append(participant)
    content = kind_specific

    return render(request, 'freports/report_detail.html',
        {'details': details, 'report': report, 'participants': participants, 'content': content, 'subjects': subjects })

@login_required(login_url='/login/')
def add_order(request, rid):
    report = Report.objects.get(pk=rid)
    courts = Court.objects.all()
    kind = 'first_arrived'
    content, judges = {}, {}
    header = u'Провадження №%s/%s' % (report.number, report.number_year)
    content['obvious_fields'] = kind_specific[kind][1]
    content['kind'] = kind

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_element = valid_data['data']
            new_element['name'] = 'first_arrived'

            case_number = request.POST.get('case')
            if not case_number:
                errors['case'] = u"Номер судової справи є обов'язковим"

            judge = request.POST.get('judge')
            if judge:
                try:
                    judge_name = Judge.objects.get(pk=judge)
                    judges = Judge.objects.filter(court_name=judge_name.court_name)
                except ObjectDoesNotExist:
                    errors['judge'] = u"Будь ласка, виберіть суддю зі списку"
            else:
                errors['judge'] = u"Вибір судді є обов'язковим"

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                new_element['case'] = case_number
                new_element['judge'] = judge
                new_element['court'] = request.POST.get('court')
                return render(request, 'freports/add_order_form.html',
                    {'header': header, 'content': content, 'new_content': new_element, 'errors': errors,
                    'courts': courts, 'judges': judges})
            else:
                new_detail = ReportEvents(**new_element)
                report.judge_name = judge_name
                report.case_number = case_number
                report.date_arrived = new_detail.date
                report.active = True
                report.change_date = datetime.utcnow().date()
                time_amount = datetime.utcnow() - datetime.strptime(report.date_arrived, "%Y-%m-%d")
                days_amount = time_amount.days
                reports = Report.objects.all()
                if len(reports) > 0:
                    new_time_amount = datetime.utcnow().date() - reports[0].change_date
                    for element in reports:
                        if element.active_days is not None:
                            element.change_date = timezone.now
                            element.active_days_amount = element.active_days_amount + new_time_amount.days

                report.active_days_amount = days_amount
                update_days_info(reports)
                report.save()
                new_detail.save()
                messages.success(request, u"Ухвала про призначення експертизи успішно додана")
                return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання ухвали про призначення експертизи скасовано")
            return HttpResponseRedirect(reverse('forensic_reports_list'))

    elif request.method == 'GET':
        if request.is_ajax():
            court = Court.objects.get(pk=request.GET.get('court'))
            judges = Judge.objects.filter(court_name=court)
            new_list = []
            for judge in judges:
                new_item = {'id': judge.id, 'short_name': judge.short_name()}
                new_list.append(new_item)
            return JsonResponse({'status': 'success', 'judges': new_list, 'court_number': court.number})
        else:
            new_content = {}
            if report.judge_name:
                judge = report.judge_name
                new_content['court'] = judge.court_name.id
                new_content['judge'] = judge.id
                if judge.court_name.number:
                    new_content['case'] = u"{}/".format(judge.court_name.number)
                judges = Judge.objects.filter(court_name=judge.court_name)

        return render(request, 'freports/add_order_form.html', {'header': header, 'content': content, 'courts': courts,
            'new_content': new_content, 'judges': judges})

@login_required(login_url='/login/')
def add_detail(request, rid, kind):
    report = Report.objects.get(pk=rid)
    details = ReportEvents.objects.filter(report=report).order_by('date').reverse()
    content, new_content = {}, {}
    header = {}
    header['main'] = u'Додавання події до провадження №%s/%s' % (report.number, report.number_year)
    header['second'] = kind_specific[kind][0].capitalize()
    content['obvious_fields'] = kind_specific[kind][1]
    if 'type' in content['obvious_fields']:
        content['select_type'] = kind_specific[kind][2]
    content['kind'] = kind
    for detail in details:
        if detail.name in ('arrived', 'first_arrived'):
            new_content['sending'] = detail.received
            break
        if detail.name == 'petition':
            new_content['received'] = detail.sending
            break

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_element = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/detail_form.html',
                    {'header': header, 'content': content, 'new_content': new_element, 'errors': errors})

            else:
                if new_element['activate'] == 'executed':
                    new_element['activate'] = False
                    report.executed = True
                    report.date_executed = new_element['date']
                    report.save()
                new_detail = ReportEvents(**new_element)
                new_detail.save()
                report.change_date = datetime.utcnow().date()
                report = check_active(report)
                report.active_days_amount = days_count(report, 'active')
                report.waiting_days_amount = days_count(report, 'waiting')
                update_dates_info(reports)

                report.save()
                messages.success(request, u"Подія '%s' успішно додана" % kind_specific[new_detail.name][0])

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання деталей провадження скасовано")

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))

    else:
        return render(request, 'freports/detail_form.html', {'header': header, 'content': content, 'new_content': new_content})

@login_required(login_url='/login/')
def edit_detail(request, rid, did):
    report = Report.objects.get(pk=rid)
    detail = ReportEvents.objects.get(pk=did)
    header = {
        'main': u'Редагування події провадження №%s/%s' % (report.number, report.number_year),
        'second': kind_specific[detail.name][0].capitalize()}
    content = {'obvious_fields': kind_specific[detail.name][1], 'kind': detail.name}
    if 'type' in content['obvious_fields']:
        content['select_type'] = kind_specific[detail.name][2]

    if request.method == 'POST':
        if request.POST.get('next'):
            next_url = reverse(request.POST.get('next'), args=[rid])
        else:
            next_url = reverse('report_details_list', args=[rid])

        if request.POST.get('save_button'):

            valid_data = valid_detail(request.POST, rid)
            errors = valid_data['errors']
            new_data = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/detail_form.html',
                    {'header': header, 'content': content, 'new_content': new_data, 'errors': errors})

            else:
                edit_detail = ReportEvents(**new_data)
                edit_detail.id = did
                if new_data['activate'] == 'executed':
                    edit_detail.activate = False
                    report.executed = True
                    report.date_executed = new_data['date']
                else:
                    edit_detail.activate = new_data['activate']
                edit_detail.save()
                report = check_active(report)
                if edit_detail.name == 'first_arrived':
                    report.date_arrived = edit_detail.date
                report.active_days_amount = days_count(report, 'active')
                report.waiting_days_amount = days_count(report, 'waiting')
                reports = Report.objects.all()
                update_dates_info(reports)
                report.save()
                messages.success(request, u"Подія '%s' успішно змінена" % kind_specific[edit_detail.name][0])

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Редагування деталей провадження скасовано")

        return HttpResponseRedirect(next_url)

    else:
        new_content = detail
        new_content.date = new_content.date.isoformat()
        if new_content.time:
            new_content.time = new_content.time.isoformat()
        if new_content.decision_date:
            new_content.decision_date = new_content.decision_date.isoformat()
        return render(request, 'freports/detail_form.html', {'new_content': new_content, 'content': content, 'header': header})

@login_required(login_url='/login/')
def delete_detail(request, rid, did):
    report = Report.objects.get(pk=rid)
    detail = ReportEvents.objects.get(pk=did)
    content = u"Ви дійсно бажаєте видалити подію '%s' до провадження №%s/017?" % (kind_specific[detail.name][0], report.number)
    header = u"Видалення події провадження №%s/%s" % (report.number, report.number_year)

    if request.method == 'GET':
        return render(request, 'freports/delete_form.html', {'report': report, 'content': content, 'header': header})

    elif request.method == 'POST':
        if request.POST.get('delete_button'):
            current_detail = detail
            current_detail.delete()

            report.change_date = datetime.utcnow().date()
            report = check_active(report)
            report.active_days_amount = days_count(report, 'active')
            report.waiting_days_amount = days_count(report, 'waiting')
            reports = Report.objects.all()
            update_dates_info(reports)
            report.save()

            messages.success(request,
                u"Подія '%s' до провадження №%s/%s успішно видалена" % (kind_specific[detail.name][0], report.number, report.number_year))
        elif request.POST.get('cancel_button'):
            messages.warning(request,
                u"Видалення події '%s' до провадження №%s/%s скасоване" % (kind_specific[detail.name][0], report.number, report.number_year))

        return HttpResponseRedirect(reverse('report_details_list', args=[rid]))


def check_active(report):
    details = ReportEvents.objects.filter(report=report).order_by('date').reverse()
    if details.count() > 1 and details[0].date == details[1].date:
        if True in (details[0].activate, details[1].activate):
            if details.count() > 2 and details[2].activate == True:
                report.active = True
        else:
            report.active = False
    else:
        last_detail = ReportEvents.objects.filter(report=report).order_by('date').reverse()[0]
        if last_detail.activate == True:
            report.active = True
        elif last_detail.activate == False:
            report.active = False
    return report

def days_count(report, status):
    events = ReportEvents.objects.filter(report=report).order_by('date')
    days_amount = 0
    last_event = events.reverse()[0]
    if status == 'active':
        event_activate = True
        for event in events:
            if event.id == events[0].id:
                before_event = events[0]
            else:
                if event.activate != event_activate and before_event.activate == event_activate:
                    time = event.date - before_event.date
                    days_amount += time.days
                if event.activate is not None:
                    before_event = event
        try:
            execution_time = report.date_executed - last_event.date
            days_amount += execution_time.days
        except TypeError:
            pass
    elif status == 'waiting':
        event_activate = False

    if last_event.activate == event_activate:
            time = date.today() - last_event.date
            days_amount += time.days

    return days_amount

def update_dates_info(reports):
    last_update = reports[0].change_date
    time_amount = date.today() - last_update
    if time_amount == 0:
        return True
    for report in reports:
        report.change_date = last_update
        if report.executed is None:
            if report.active:
                report.active_days_amount += time_amount.days
            else:
                report.waiting_days_amount += time_amount.days
            report.save()

def valid_detail(request_info, report_id):
    errors = {}
    new_element = {}

    report = Report.objects.filter(pk=report_id)
    if len(report) != 1:
        errors['report'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте пізніше'
    else:
        new_element['report'] = report[0]

    name = request_info.get('name')
    if name in ['first_arrived', 'arrived', 'petition', 'bill', 'paid', 'schedule', 'inspected', 'done']:
        new_element['name'] = request_info.get('name')
    else:
        errors['name'] = u"На сервер відправлені неправельні дані. Будь-ласка спробуйте пізніше"

    date = request_info.get('date')
    if not date:
        errors['date'] = u"Дата події є обов'язковою"
    else:
        try:
            new_element['date'] = date
        except ValueError:
            errors['date'] = u"Введіть коректний формат дати"

    if name == 'first_arrived':
        decision_date = request_info.get('decision_date')
        if not decision_date:
            errors['decision_date'] = u"Дата винесення ухвали є обов'язковою"
        else:
            try:
                new_element['decision_date'] = decision_date
            except ValueError:
                errors['decision_date'] = u"Введіть коректний формат дати"

    if name in ['first_arrived', 'arrived']:
        received = request_info.get('received')
        if not received:
            errors['received'] = u"Інформація про отримані матеріали є обов'язковою"
        else:
            new_element['received'] = received

    if name in ['petition', 'bill', 'paid', 'done', 'inspected']:
        subspecies = request_info.get('subspecies')
        if not subspecies:
            errors['subspecies'] = u"Інформація про підтип події є обов'язковою"
        else:
            new_element['subspecies'] = subspecies

    if name in ['schedule']:
        time = request_info.get('time')
        if not time:
            errors['time'] = u"Дата та час огляду є обов'язковими"
        else:
            try:
                new_element['time'] = time
            except ValueError:
                errors['time'] = u"Введіть коректний формат дати та часу"

    if name == 'petition':
        necessary = request_info.get('necessary')
        if not necessary:
            errors['necessary'] = u"Інформація про зміст клопотання є обов'язковою"
        else:
            new_element['necessary'] = necessary

    if name == 'bill':
        cost = request_info.get('cost')
        if not cost:
            errors['cost'] = u"Інформація про вартість роботи є обов'язковою"
        else:
            try:
                new_element['cost'] = int(cost)
            except ValueError:
                errors['cost'] = u"Введіть вартість в числовому вигляді"
                new_element['cost'] = cost

    new_element['sending'] = request_info.get('sending')
    new_element['address'] = request_info.get('address', '')
    new_element['info'] = request_info.get('info')

    activate_true_list = ['first_arrived', 'arrived', 'paid', 'inspected']
    if name in activate_true_list:
        new_element['activate'] = True
    elif name == u'done':
        new_element['activate'] = 'executed'
    else:
        new_element['activate'] = False

    return {'errors': errors, 'data': new_element}

