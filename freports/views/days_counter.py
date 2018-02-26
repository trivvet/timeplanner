# days count
from datetime import date, datetime

from ..models import ReportEvents

def check_active(report):
    details = ReportEvents.objects.filter(report=report).order_by('date')
    last_detail = details[details.count() - 1]
    if last_detail.name == 'done':
        report.active = False
        report.executed = True
        report.date_executed = last_detail.date
    elif last_detail.activate:
        report.active = True
        report.executed = False
    else:
        report.active = False
        report.executed = False

    return report

def days_count(report, status):
    events = ReportEvents.objects.filter(report=report).order_by('date')
    days_amount = 0
    if events.count() > 0:
        event_activate = False
        last_event = events.reverse()[0]
        if status == 'active':
            event_activate = True
            before_event = events[0]
            if events.count > 1:
                for event in events:
                    if event.activate != True and before_event.activate == True:
                        time = event.date - before_event.date
                        days_amount += time.days
                    before_event = event
            if before_event.activate:
                time = date.today() - before_event.date
                days_amount += time.days

        if status != 'active' and last_event.activate == False:
            time = date.today() - last_event.date
            days_amount += time.days

    return days_amount

def update_dates_info(reports):
    reports = reports.filter(executed=False)
    last_update = reports[0].change_date
    time_amount = date.today() - last_update
    if time_amount == 0:
        return True
    for report in reports:
        report.change_date = date.today()
        if report.active:
            report.active_days_amount = days_count(report, 'active')
        else:
            report.waiting_days_amount = days_count(report, 'waiting')
        report.save()


