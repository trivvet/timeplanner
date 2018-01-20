# days count
from datetime import date

from ..models import ReportEvents

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
    if events.count() == 0:
        return 0
    days_amount = 0
    event_activate = False
    last_event = events.reverse()[0]
    if status == 'active':
        event_activate = True
        before_event = events[0]
        for event in events:
            if event.activate != True and before_event.activate == True:
                time = event.date - before_event.date
                days_amount += time.days
            before_event = event

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
            report.active_days_amount += time_amount.days
        else:
            report.waiting_days_amount += time_amount.days
        report.save()


