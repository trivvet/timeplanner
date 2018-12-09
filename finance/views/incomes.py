# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.views.generic.detail import SingleObjectTemplateResponseMixin
from django.views.generic.edit import CreateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator

from ..models import Income, Order
from ..forms import IncomeForm

class JSONResponseMixin:
    def render_to_json_response(self, context, **response_kwargs):
        return JsonResponse(
            self.get_data(context),
            safe=False
        )

    def get_data(self, context):
        order_id = context.get("order_id")
        order = Order.objects.get(pk=order_id)
        data_serialized = serializers.serialize('json', [order, ])
        return data_serialized

@login_required(login_url='/login/')
def incomes_list(request):
    incomes = Income.objects.all()
    return render(request, 'finance/incomes_list.html', 
        {'incomes': incomes})

@method_decorator(login_required, name='dispatch')
class IncomeCreate(JSONResponseMixin, CreateView):
    template_name = 'finance/form.html'
    form_class = IncomeForm
    success_url = reverse_lazy('finance:incomes_list')

    def get_context_data(self, **kwargs):
        context = super(IncomeCreate, self).get_context_data(**kwargs)
        context['header'] = u"Додавання надходження"
        return context

    def render_to_response(self, context):
        # import pdb;pdb.set_trace()
        # Look for a 'format=json' GET argument
        if self.request.GET.get('format') == 'json':
            print type(self.render_to_json_response(self.request.GET))
            return self.render_to_json_response(self.request.GET)
        else:
            return super(IncomeCreate, self).render_to_response(context)

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