# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.

def first_page(request):
    return render(request, 'business_card/home.html', {})
