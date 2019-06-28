# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

try:
    from timeplanner.sensitive_data import GOOGLE_API
except ImportError:
	GOOGLE_API = ""

# Create your views here.

def first_page(request):
    google_api = GOOGLE_API
    return render(request, 'business_card/home.html', 
        {'google_api': google_api})
