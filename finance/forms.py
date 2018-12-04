# -*- coding: utf-8 -*-
from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Layout, ButtonHolder

from .models import Income

class IncomeForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(IncomeForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.form_method = 'post'
        self.helper.label_class = 'col-sm-4'
        self.helper.field_class = 'col-sm-6'

        self.helper.add_input(
            Submit('submit', u'Зберегти', 
                # css_class='btn btn-primary'
                ))
        self.helper.add_input(
            Submit('cancel', u'Скасувати'))

    class Meta:
        model = Income
        fields = ['order', 'date', 'account', 'amount', 'payer']





        # self.helper.form_class = 'form-horizontal'
        # self.helper.form_method = 'post'
        # self.helper.form_action = 'submit_survey'

        # self.helper.add_input(Submit('submit', 'Submit'))