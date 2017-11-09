# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist

from ..models import Court, Judge

@login_required(login_url='/login/')
def courts_list(request):
    courts = Court.objects.all().order_by('name')
    header = 'Список судів'
    return render(request, 'freports/courts_list.html', {'courts': courts, 'header': header})

@login_required(login_url='/login/')
def add_court(request):
    header = u'Додавання суду'
    if request.method == 'POST':
        if request.POST.get('save_button'):
            valid_data = valid_court(request.POST)
            errors = valid_data['errors']
            new_court = valid_data['new_court']
            if errors:
                messages.error(request, u"Виправте наступні помилки")
                return render(request, 'freports/court_form.html', {'content': new_court, 'errors': errors, 'header': header})
            else:
                new_item = Court(**new_court)
                new_item.save()
                messages.success(request, u"%s успішно доданий" % new_item)
        elif request.POST.get('cancel_button'):
            messages.warning(request, u"Додавання суду скасовано")

        return HttpResponseRedirect(reverse('courts_list'))

    else:
        return render(request, 'freports/court_form.html', {'header': header})


def delete_court(request, cid):
    court = Court.objects.get(pk=cid)
    header = u"Видалення інформації про %s" % court
    if request.method == "GET":
        return render(request, 'freports/delete_form.html', {'content': court, 'header': header})
    else:
        if request.POST.get('cancel_button'):
            messages.warning(request, u"Видалення суду скасовано")
        elif request.POST.get('delete_button'):
            court.delete()
            messages.success(request, u"%s успішно видалений" % court)

        return HttpResponseRedirect(reverse('courts_list'))


def valid_court(request_info):
    errors, new_court = {}, {}
    name = request_info['name']
    if not name:
        errors['name'] = u"Назва суду є обов'язковою"
    else:
        new_court['name'] = name

    number = request_info['number']
    try:
        new_court['number'] = int(number)
    except ValueError:
        new_court['number'] = None

    new_court['address'] = request_info['address']

    chair = request_info.get('chair')
    if chair:
        try:
            new_court['chair'] = Judge.objects.get(pk=chair)
        except ObjectDoesNotExist:
            errors['chair'] = u"Будь ласка, виберіть суддю зі списку"

    return {'new_court': new_court, 'errors': errors}
