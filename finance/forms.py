# -*- coding: utf-8 -*-
from django import forms
from django.db import models

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button

from .models import Income, Order, Account, Execution

class IncomeForm(forms.ModelForm):

    date = forms.DateField(
        label=u"Дата отримання",
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'id': 'inputDate3',
                'data-toggle': 'datetimepicker',
                'data-target': "#inputDate3"}
            )
        )

    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-6'

        self.helper.layout.append(Layout(
            FormActions(
                Submit('submit', u'Зберегти'),
                Button('submit', u'Скасувати', 
                    css_class='btn-link'),
            )
        ))

    class Meta:
        model = Income
        fields = ['order', 'date', 'account', 'amount', 'payer']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        order = self.cleaned_data['order']
        remainder = order.total_sum - order.paid_sum + self.initial.get('amount', 0)
        if amount > remainder:
            raise forms.ValidationError(
                u"Сума усіх надходжень не може бути більша кошторисної вартості замовлення!")
        return amount


class ExecutionForm(forms.ModelForm):
    date = forms.DateField(
        label=u"Дата виконання",
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'id': 'inputDate3',
                'data-toggle': 'datetimepicker',
                'data-target': "#inputDate3"}
            )
        )

    def __init__(self, *args, **kwargs):
        super(ExecutionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper(self)

        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-6'

        self.helper.layout.append(Layout(
            FormActions(
                Submit('submit', u'Зберегти'),
                Button('submit', u'Скасувати', 
                    css_class='btn-link'),
            )
        ))

    class Meta:
        model = Execution
        fields = ['order', 'date', 'account', 'amount', 'closed_tasks']

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        order = self.cleaned_data['order']
        remaider = order.total_sum - order.done_sum + self.initial.get('amount', 0)
        if amount > remaider:
            raise forms.ValidationError(
                u"Сума усіх виконань не може бути більша кошторисної вартості замовлення!")
        return amount

    def clean_date(self):
        date = self.cleaned_data['date']
        order_id = self.data['order']
        incomes = Income.objects.filter(order=order_id)
        if incomes:
            first_income = incomes.order_by('date').first()
            if date < first_income.date:
                raise forms.ValidationError(
                    u"Виконання не може бути раніше дня першого надходження по замовленню")
        return date

        

