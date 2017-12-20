# days count
from datetime import date

def active_days(report, details):
    days_amount = 0
    if details.count() > 0:
        before_detail = details[0]
        for detail in details:
            if detail.activate == False and before_detail.activate == True:
                time = detail.date - before_detail.date
                days_amount += time.days
            if detail.activate is not None:
                before_detail = detail

    try:
        time = report.date_executed - report.last_event.date
        days_amount += time.days
    except TypeError:
        pass
    if details.count() == 0 or detail.activate == True:
        time = date.today() - report.last_event.date
        days_amount += time.days

    return days_amount

def waiting_days(report):
    if report.executed != True and report.active == False:
        waiting_time = date.today() - report.last_event.date
        days = waiting_time.days
    else:
        days = None

    return days


def days_amount(reports):
    for report in reports:
        details = ReportEvents.objects.filter(report=report).order_by('date')
        report.last_event = details.reverse()[0]
        report.days_amount = active_days(report, details)
        report.waiting_time = waiting_days(report)

    return reports

