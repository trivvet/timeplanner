# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

def reports_list(request):
    return render(request, 'freports/reports_list.html')

