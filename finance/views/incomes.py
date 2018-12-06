# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from ..models import Income
from ..forms import IncomeForm

@login_required(login_url='/login/')
def incomes_list(request):
    incomes = Income.objects.all()
    return render(request, 'finance/incomes_list.html', 
        {'incomes': incomes})

@method_decorator(login_required, name='dispatch')
class IncomeCreate(CreateView):
    template_name = 'finance/form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('finance:incomes_list')

    def get_context_data(self, **kwargs):
        context = super(IncomeCreate, self).get_context_data(**kwargs)
        context['header'] = u"Додавання надходження"
        return context

    def form_valid(self, form):
        order = form.instance.order
        order.status = 'active'
        order.save()
        return super(IncomeCreate, self).form_valid(form)

class IncomeDelete(DeleteView):
    model = Income
    template_name = 'finance/confirm_delete.html'
    success_url = reverse_lazy('finance:incomes_list')

    def get_context_data(self, **kwargs):
        context = super(IncomeDelete, self).get_context_data(**kwargs)
        context['header'] = u"Видалення надходження"
        return context

    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        order = self.object.order
        order.status = 'inactive'
        order.save()
        return super(IncomeDelete, self).delete(
            self, request, *args, **kwargs)