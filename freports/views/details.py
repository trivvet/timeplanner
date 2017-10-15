# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages

from ..models import Report

def details_list(request, rid):
    content = {}
    content['report'] = rid
    
    return render(request, 'freports/report_detail.html', {'content': content})

def add_detail(request, rid):
    if request.method == 'POST':
        if request.POST.get('save_button'):
            errors = {}

            if errors:
                messages.error(request, "Виправте наступні недоліки")
                return render(request, 'freports/detail_form.html', {})

            else:
                messages.success(request, "Подія '%s' успішно додана" % 'Додавання')

        elif request.POST.get('cancel_button'):
            messages.warning(request, "Додавання деталей провадження скасовано")
            
        return HttpResponseRedirect(reverse('report_details_list', args=rid))

    else:
        content = rid
        return render(request, 'freports/detail_form.html', {'content': content})
