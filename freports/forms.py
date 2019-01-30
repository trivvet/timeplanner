# -*- coding: utf-8 -*-
from django import forms
from django.db import models

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, Button

from .models import Research

STATUS_CHOICES = (
    ('active', u'Активний'),
    ('noactive', u'Призупинений'),
    ('done', u'Виконаний'),
)

class ResearchForm(forms.ModelForm):
    status = forms.ChoiceField(
        label=u"Статус дослідження",
        widget=forms.RadioSelect(),
        choices=STATUS_CHOICES)

    date_arrived = forms.DateField(
        label=u"Дата надходження заяви",
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'id': 'inputDate',
                'data-toggle': 'datetimepicker',
                'data-target': "#inputDate"
                }
            )
        )

    date_executed = forms.DateField(
        label=u"Дата виконання дослідження",
        widget=forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={
                'id': 'inputDate2',
                'data-toggle': 'datetimepicker',
                'data-target': "#inputDate2"
                }
            )
        )

    def __init__(self, *args, **kwargs):
        super(ResearchForm, self).__init__(*args, **kwargs)
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
        model = Research
        fields = ['date_arrived', 'address', 'applicant', 'object_name', 
        'research_kind']