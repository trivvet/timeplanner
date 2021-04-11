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

from .days_counter import check_active, days_count, update_dates_info
from ..models import (
    Report, 
    ReportEvents, 
    ReportParticipants, 
    ReportSubject, 
    Court, 
    Judge, 
    Task
    )
from .tasks import add_detail_task, edit_detail_task

from finance.models import Order, Income, Account
from finance.views import (
    order_auto_create,
    order_auto_edit,
    income_auto_create,
    income_auto_edit
    )

petition_type = [
    u'Про надання додаткових матеріалів', 
    u'Про уточнення питань', 
    u'Про надання справи'
    ]
done_type = [
    u'Висновок експерта', 
    u'Повідомлення про неможливість', 
    u'Залишення без виконання'
    ]
inspected_type = [
    u'Проведено успішно', 
    u'Не надано доступ', 
    u'Відмінено'
    ]
bill_type = [
    u'Направлено рекомендованого листа', 
    u'Вручено особисто', 
    u'Вручено представнику', 
    u'Направлено електронного листа'
    ]
message_type = [
    u'Направлене клопотання', 
    u'Надіслані листи', 
    u'Повідомлено телефоном', 
    u'Повідомлено особисто'
    ]
kind_specific = {
        'first_arrived': [
            u'Надходження ухвали', 
            ['date', 'info', 'received', 'way_forward', 'decision_date']
            ],
        'petition': [
            u'Направлення клопотання', 
            ['date', 'info', 'type', 'necessary', 'sending'], 
            petition_type
            ],
        'arrived': [
            u'Надходження з суду', 
            ['date', 'info', 'received', 'way_forward']
            ],
        'bill': [
            u'Направлення рахунку', 
            ['date', 'info', 'cost', 'address', 'type'], 
            bill_type
            ],
        'paid': [
            u'Оплата', 
            ['date', 'info', 'account'], 
            ],
        'schedule': [
            u'Призначення виїзду', 
            ['date', 'info', 'time', 'type'],
            message_type
            ],
        'inspected': [
            u'Проведення огляду', 
            ['date', 'info', 'type'], 
            inspected_type
            ],
        'done': [
            u'Відправлення до суду', 
            ['date', 'info', 'sending', 'type'], 
            done_type
            ]
        }

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
    details = ReportEvents.objects.filter(report=report).order_by('date', 'id')
    content = {}

    if len(details.filter(name='first_arrived')) < 1:
        return HttpResponseRedirect(reverse('freports:add_order', args=[rid]))

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
    content['kind_specific'] = kind_specific
    time_after_update = date.today() - report.change_date
    report.time_after_update = time_after_update.days
    tasks = Task.objects.filter(report=report).exclude(execute=True)

    return render(request, 'freports/report_detail.html',
        {'details': details, 'report': report, 'participants': participants, 
        'content': content, 'subjects': subjects, 'tasks': tasks})

@login_required(login_url='/login/')
def add_order(request, rid):
    report = Report.objects.get(pk=rid)
    courts = Court.objects.all().order_by('name')
    kind = 'first_arrived'
    content, judges = {}, {}
    header = u'по провадженню №%s' % (report.full_number())
    content['obvious_fields'] = kind_specific[kind][1]
    content['kind'] = kind
    content['number_year'] = report.number_year

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
                new_detail.save()
                report.judge_name = judge_name
                report.case_number = case_number
                report.date_arrived = new_detail.date
                report.active = True
                report.change_date = datetime.utcnow().date()
                
                report.active_days_amount = days_count(report, 'active')
                report.waiting_days_amount = days_count(report, 'waiting')
                reports = Report.objects.all()
                update_dates_info(reports)
                
                report.save()
                new_detail.save()
                messages.success(request, u"Ухвала про призначення експертизи успішно додана")
                return HttpResponseRedirect(reverse(
                    'freports:report_detail', args=[rid]))

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання ухвали про призначення експертизи скасовано")
        elif request.POST.get('delete_button'):
                report.delete()
                messages.success(request, u"Провадження №%s/017 успішно видалено" % report.number)

        return HttpResponseRedirect(reverse('freports:reports_list'))

    elif request.method == 'GET':
        if request.is_ajax() and request.GET.get('court', ''):
            court = Court.objects.get(pk=request.GET.get('court'))
            judges = Judge.objects.filter(court_name=court).order_by('surname')
            new_list = []
            for judge in judges:
                new_item = {'id': judge.id, 
                    'short_name': judge.short_name()}
                new_list.append(new_item)
            return JsonResponse({'status': 'success', 
                'judges': new_list, 'court_number': court.number})
        else:
            new_content = {}
            if report.judge_name:
                judge = report.judge_name
                new_content['court'] = judge.court_name.id
                new_content['judge'] = judge.id
                if judge.court_name.number:
                    new_content['case'] = u"{}/".format(judge.court_name.number)
                judges = Judge.objects.filter(court_name=judge.court_name)

        return render(request, 'freports/add_order_form.html', {
            'header': header, 'content': content, 'courts': courts,
            'new_content': new_content, 'judges': judges})

@login_required(login_url='/login/')
def add_detail(request, rid, kind):
    report = Report.objects.get(pk=rid)
    details = ReportEvents.objects.filter(
        report=report).order_by('date').reverse()
    content, new_content = {}, {}
    header = {}
    header['main'] = u'Додавання події до провадження №%s/%s' % (report.number, report.number_year)
    header['second'] = kind_specific[kind][0].capitalize()
    content['obvious_fields'] = kind_specific[kind][1]
    if 'type' in content['obvious_fields']:
        content['select_type'] = kind_specific[kind][2]
    if 'account' in content['obvious_fields']:
        content['accounts'] = Account.objects.filter(status='work')
    content['kind'] = kind
    for detail in details:
        if detail.name in ('arrived', 'first_arrived'):
            new_content['sending'] = detail.received
            break
        if detail.name == 'petition':
            new_content['received'] = detail.sending
            break
    if kind == 'inspected' and details[0].time:
        new_content['date'] = details[0].time.date().isoformat()
    else:
        new_content['date'] = details[0].date.isoformat()

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
                reports = Report.objects.all()
                update_dates_info(reports)
                if new_detail.name == 'bill':
                    report.cost = new_detail.cost
                    new_order = order_auto_create(new_detail)
                    new_order.save()
                report.save()
                # if new_detail.name == 'paid':
                    #n ew_income = income_auto_create(new_detail)
                    # new_income.save()
                add_detail_task(new_detail)
                messages.success(request, u"Подія '%s' успішно додана" % kind_specific[new_detail.name][0])

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання деталей провадження скасовано")

        return HttpResponseRedirect(reverse('freports:report_detail',
            args=[rid]))

    else:
        return render(request, 'freports/detail_form.html', {
            'header': header, 'content': content, 
            'new_content': new_content})

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
    if 'account' in content['obvious_fields']:
        content['accounts'] = Account.objects.filter(status='work')
    if request.method == 'POST':
        if request.POST.get('next'):
            next_url = reverse(request.POST.get('next'), args=[rid])
        else:
            next_url = reverse('freports:report_detail', args=[rid])

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
                if edit_detail.name == 'bill':
                    report.cost = edit_detail.cost
                    edit_order = order_auto_edit(edit_detail)
                    edit_order.save()
                report.save()
                edit_detail_task(edit_detail)
                messages.success(request, u"Подія '%s' успішно змінена" % kind_specific[edit_detail.name][0])

        elif request.POST.get('cancel_button'):
            messages.warning(request, 
                u"Редагування деталей провадження скасовано")

        return HttpResponseRedirect(next_url)

    else:
        new_content = detail
        new_content.date = new_content.date.isoformat()
        if new_content.time:
            new_content.time = timezone.localtime(new_content.time).isoformat()
        if new_content.decision_date:
            new_content.decision_date = new_content.decision_date.isoformat()
        return render(request, 'freports/detail_form.html', 
            {'new_content': new_content, 'content': content, 'header': header})

@login_required(login_url='/login/')
def delete_detail(request, rid, did):
    report = Report.objects.get(pk=rid)
    detail = ReportEvents.objects.get(pk=did)
    content = u"Ви дійсно бажаєте видалити подію '%s' до провадження №%s/017?" % (kind_specific[detail.name][0], report.number)
    header = u"Видалення події провадження №%s/%s" % (report.number, report.number_year)

    if request.method == 'GET':
        return render(request, 'freports/delete_form.html', 
            {'report': report, 'content': content, 'header': header})

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
            if current_detail.name == 'bill':
                report.cost = None
                try:
                    order = Order.objects.get(report=current_detail.report)
                    order.delete()
                except:
                    pass
            report.save()

            messages.success(request,
                u"Подія '%s' до провадження №%s/%s успішно видалена" % (kind_specific[detail.name][0], report.number, report.number_year))
        elif request.POST.get('cancel_button'):
            messages.warning(request,
                u"Видалення події '%s' до провадження №%s/%s скасоване" % (kind_specific[detail.name][0], report.number, report.number_year))

        return HttpResponseRedirect(reverse('freports:report_detail',
            args=[rid]))

def valid_detail(request_info, report_id):
    errors = {}
    new_element = {}

    report = Report.objects.filter(pk=report_id)
    if len(report) != 1:
        errors['report'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте пізніше'
    else:
        new_element['report'] = report[0]
    
    allowed_names = (
        'first_arrived', 
        'arrived', 
        'petition', 
        'bill', 
        'paid', 
        'inspected', 
        'done'
    )

    name = request_info.get('name')
    if name in allowed_names:
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
        
        way_forward = request_info.get('way_forward')
        if way_forward:
            new_element['way_forward'] = way_forward

    if name in ['petition', 'bill', 'done', 'inspected']:
        subspecies = request_info.get('subspecies')
        if not subspecies:
            errors['subspecies'] = u"Інформація про підтип події є обов'язковою"
        else:
            new_element['subspecies'] = subspecies

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

    if name == 'paid':
        account = Account.objects.get(pk=request_info.get('account'))
        subspecies = u'На рахунок {}'.format(
            account.title)
        new_element['subspecies'] = subspecies

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

@login_required(login_url='/login/')
def add_schedule(request, rid):
    report = Report.objects.get(pk=rid)
    details = ReportEvents.objects.filter(
        report=report).order_by('date').reverse()
    participants = ReportParticipants.objects.filter(
        report=report)
    content, start_date = {}, {}
    content['report_number'] = report.full_number
    content['participants'] = participants

    start_date = details[0].date.isoformat()

    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_schedule(request.POST, rid)
            errors = valid_data['errors']
            new_element = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/schedule_form.html',
                    {'errors': errors, 'content': content, 
                     'new_content': new_element})

            else:
                new_schedule = ReportEvents(**new_element)
                new_schedule.save()
                report.change_date = datetime.utcnow().date()
                report = check_active(report)
                report.active_days_amount = days_count(report, 'active')
                report.waiting_days_amount = days_count(report, 'waiting')
                reports = Report.objects.all()
                update_dates_info(reports)
                report.save()
                add_detail_task(new_schedule)
                messages.success(request, u"Виїзд успішно призначений")

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання призначення виїзду скасовано")

        return HttpResponseRedirect(reverse('freports:report_detail',
            args=[rid]))

    else:
        return render(request, 'freports/schedule_form.html', {
            'content': content, 'start_date': start_date})


def valid_schedule(request_info, report_id):
    errors = {}
    new_element = {}

    report = Report.objects.filter(pk=report_id)
    if len(report) != 1:
        errors['report'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте пізніше'
    else:
        new_element['report'] = report[0]

    new_element['name'] = 'schedule'

    date = request_info.get('date')
    if not date:
        errors['date'] = u"Дата події є обов'язковою"
    else:
        try:
            new_element['date'] = date
        except ValueError:
            errors['date'] = u"Введіть коректний формат дати"

    time = request_info.get('time')
    pz = timezone.get_current_timezone()
    if not time:
        errors['time'] = u"Дата та час огляду є обов'язковими"
    else:
        try:
            naive_time = datetime.strptime(time, '%Y-%m-%d %H:%M')
            new_element['time'] = pz.localize(naive_time)
        except ValueError:
            errors['time'] = u"Введіть коректний формат дати та часу"

    new_element['subspecies'] = u"Направлене клопотання"

    participants = request_info.getlist('persons')
    call_types = request_info.getlist('callType')
    addresses = request_info.getlist('address')
    letters = request_info.getlist('letter')

    info = request_info.get('info')

    if participants:
        letter_number = 0
        for idx, participant in enumerate(participants):
            try:
                person = ReportParticipants.objects.get(pk=participant)
                if(addresses[idx]):
                    if idx != 0 or info:
                        info += '; '
                    if call_types[idx] == 'letter':
                        if letters[letter_number]:
                            info += u"{} (Направлено лист №{} на адресу {})".format(
                                person.full_name(), letters[letter_number], addresses[idx])
                        else:
                            info += u"{} (Направлено лист на адресу {})".format(
                                person.full_name(), addresses[idx])
                        letter_number += 1
                        person.address = addresses[idx]
                        person.save()
                    elif call_types[idx] == 'agent':
                        info += u"{} (Вручено представнику {});".format(
                            person.full_name(), addresses[idx])
                    elif call_types[idx] == 'call':
                        info += u"{} (Повідомлено дзвінком на номер {})".format(
                            person.full_name(), addresses[idx])
                        person.phone = addresses[idx]
                        person.save()
                    elif call_types[idx] == 'viber':
                        info += u"{} (Наплавлено viber-повідомлення на номер {})".format(
                            person.full_name(), addresses[idx])
                        person.phone = addresses[idx]
                        person.save()
                    else:
                        errors['person'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте ще раз'
                else:
                    errors['person'] = u'Будь-ласка введдіть додаткову інформацію'
            except IndexError:
                errors['person'] = u'Будь ласка оберіть спосіб інформування'
            except ValueError:
                errors['person'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте ще раз'    
        if not errors:
            info += '.'
            new_element['info'] = info
        else:
            if participants:
                participants = list(map(int, participants))
                new_element['active_participants'] = participants
                new_element['call_types'] = call_types
            new_element['info'] = request_info.get('info')
    
    
    new_element['activate'] = False

    if errors:
        new_element['time'] = time

    return {'errors': errors, 'data': new_element}


@login_required(login_url='/login/')
def add_bill(request, rid):
    report = Report.objects.get(pk=rid)
    details = ReportEvents.objects.filter(
        report=report).order_by('date').reverse()
    participants = ReportParticipants.objects.filter(
        report=report)
    content, start_date = {}, {}
    content['report_number'] = report.full_number
    content['participants'] = participants
    start_date = details[0].date.isoformat()
    if request.method == 'POST':
        if request.POST.get('save_button'):

            valid_data = valid_bill(request.POST, rid)
            errors = valid_data['errors']
            new_element = valid_data['data']

            if errors:
                messages.error(request, u"Виправте наступні недоліки")
                return render(request, 'freports/report_bill_form.html',
                    {'errors': errors, 'content': content, 
                     'new_content': new_element})

            else:
                new_bill = ReportEvents(**new_element)
                new_bill.save()
                report.change_date = datetime.utcnow().date()
                report = check_active(report)
                report.active_days_amount = days_count(report, 'active')
                report.waiting_days_amount = days_count(report, 'waiting')
                reports = Report.objects.all()
                update_dates_info(reports)
                report.save()
                add_detail_task(new_bill)
                messages.success(request, u"Направлення рахунку успішно зареєстровано")

        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання направлення рахунку скасовано")

        return HttpResponseRedirect(reverse('freports:report_detail',
            args=[rid]))
    else:
        return render(request, 'freports/report_bill_form.html', {
            'content': content, 'start_date': start_date})


def valid_bill(request_info, report_id):
    errors = {}
    new_element = {}

    report = Report.objects.filter(pk=report_id)
    if len(report) != 1:
        errors['report'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте пізніше'
    else:
        new_element['report'] = report[0]

    new_element['name'] = 'bill'

    date = request_info.get('date')
    if not date:
        errors['date'] = u"Дата події є обов'язковою"
    else:
        try:
            new_element['date'] = date
        except ValueError:
            errors['date'] = u"Введіть коректний формат дати"

    cost = request_info.get('cost')
    if not cost:
        errors['cost'] = u"Інформація про вартість роботи є обов'язковою"
    else:
        try:
            new_element['cost'] = int(cost)
        except ValueError:
            errors['cost'] = u"Введіть вартість в числовому вигляді"
            new_element['cost'] = cost

    participants = request_info.getlist('persons')
    call_types = request_info.getlist('callType')
    addresses = request_info.getlist('address')
    letters = request_info.getlist('letter')

    info = request_info.get('info')

    if participants:
        letter_number = 0
        for idx, participant in enumerate(participants):
            try:
                person = ReportParticipants.objects.get(pk=participant)
                if(addresses[idx]):
                    if idx != 0:
                        info += '; '
                    if call_types[idx] == 'letter':
                        if letters[letter_number]:
                            info += u"{} (Направлено лист №{} на адресу {})".format(
                                person.full_name(), letters[letter_number], addresses[idx])
                        else:
                            info += u"{} (Направлено лист на адресу {})".format(
                                person.full_name(), addresses[idx])
                        letter_number += 1
                        person.address = addresses[idx]
                        person.save()
                    elif call_types[idx] == 'agent':
                        info += u"{} (Вручено представнику {});".format(
                            person.full_name(), addresses[idx])
                    elif call_types[idx] == 'personally':
                        info += u"{} (Вручено особисто)".format(
                            person.full_name())
                    elif call_types[idx] == 'viber':
                        info += u"{} (Наплавлено viber-повідомлення на номер {})".format(
                            person.full_name(), addresses[idx])
                        person.phone = addresses[idx]
                        person.save()
                    else:
                        errors['person'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте ще раз'
                else:
                    errors['person'] = u'Будь-ласка введдіть додаткову інформацію'
            except IndexError:
                errors['person'] = u'Будь ласка оберіть спосіб інформування'
            except ValueError:
                errors['person'] = u'На сервер відправлені неправельні дані. Будь-ласка спробуйте ще раз'    
        if not errors:
            info += '.'
            new_element['info'] = info
        else:
            if participants:
                participants = list(map(int, participants))
                new_element['active_participants'] = participants
                new_element['call_types'] = call_types
            new_element['info'] = request_info.get('info')
    
    new_element['activate'] = False

    return {'errors': errors, 'data': new_element}


