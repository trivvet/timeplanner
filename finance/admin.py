# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import (
	Execution,
	Account,
	Income,
	Order
	)

class OrderAdmin(admin.ModelAdmin):
    ordering = ['name']

class ExecutionAdmin(admin.ModelAdmin):
    ordering = ['date']
    list_display = ['date', 'order', 'account', 'amount']
    list_filter = ['order']

class IncomeAdmin(admin.ModelAdmin):
    ordering = ['date']
    list_display = ['date', 'order', 'account', 'amount']
    list_filter = ['order']



# Register your models here.
admin.site.register(Execution, ExecutionAdmin)
admin.site.register(Account)
admin.site.register(Income, IncomeAdmin)
admin.site.register(Order, OrderAdmin)

