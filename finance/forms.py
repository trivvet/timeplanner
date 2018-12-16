# -*- coding: utf-8 -*-
from django import forms
from django.db import models

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button

from .models import Income, Order, Account

class IncomeForm(forms.ModelForm):
    # order = forms.ModelChoiceField(
    #     label=u"Замовлення",
    #     queryset=Order.objects.filter(status="inactive"))

    date = forms.DateField(
        label=u"Дата отримання",
        # input_formats='%Y-%m-%d',
        widget=forms.DateInput(attrs={
            'id': 'inputDate',
            'data-toggle': 'datetimepicker',
            'data-target': "#inputDate"}))

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

        

