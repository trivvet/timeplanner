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


