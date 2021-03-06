# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from django.urls import reverse
from django.contrib.admin import AdminSite
from django.contrib.auth.models import User

from axes.models import AccessAttempt, AccessLog

from .models import Report, Research

# Register your models here.
@admin.register(Report, Research)
class ReportAdmin(admin.ModelAdmin):
	pass


class MyAdminSite(AdminSite):
	site_url = "/"


admin_site = MyAdminSite(name="myadmin")
admin_site.register(Report)
admin_site.register(Research)
admin_site.register(User)
admin_site.register(AccessAttempt)
admin_site.register(AccessLog)

