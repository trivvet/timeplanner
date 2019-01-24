# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.list import ListView

from ..models import Report, Research

@method_decorator(login_required, name='dispatch')
class ResearchListView(ListView):
    model = Research
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super(ResearchListView, self).get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context


@method_decorator(login_required, name='dispatch')
class ResearchDetailView(DetailView):
    model = Research
    template_name = "freports/research_detail.html"

@login_required(login_url='/login/')
def add_new_research(request):
    header = u'Зазначте номер нового експертного дослідження'

    if request.method == 'POST':
        if request.POST.get('save_button'):
            data = request.POST
            errors, new_data = {}, {}

            if data['number']:
                try:
                    new_data['number'] = int(data['number'])
                except ValueError:
                    errors['number'] = u"Будь-ласка введіть ціле число"
                    new_data['number'] = data['number']
            else:
                errors['number'] = u"Номер висновку є обов'язковим"

            if errors:
                messages.error(request, "Виправте наступні недоліки")
                return render(request, 'freports/add_new_research.html', 
                    {'header': header, 'errors': errors,
                    'content': new_data})
            else:
                new_data['number_year'] = data['number_year']
                new_data['address'] = u"-"
                new_data['applicant'] = u"-"
                new_data['object_name'] = u"-"
                new_data['research_kind'] = u"-"
                new_data['active'] = None
                new_research = Research(**new_data)
                new_research.save()

                messages.success(request, "Дослідження №%sед/%s успішно створене" % (
                    new_research.number, new_research.number_year))
        elif request.POST.get('cancel_button'):
            messages.warning(request, "Створення нового дослідження скасовано")
        return HttpResponseRedirect(reverse('freports:researches_list'))

    else:
        last_report = Report.objects.all().order_by('number').last()
        last_research = Research.objects.all().order_by('number').last()
        content = {}
        if not last_research or last_report.number > last_research.number:
            content['number'] = last_report.number + 1
        elif last_report.number < last_research.number:
            content['number'] = last_research.number + 1
        return render(request, 'freports/add_new_research.html', 
            {'header': header, 'content': content})


@method_decorator(login_required, name='dispatch')
class ResearchCreate(CreateView):
    model = Research
    fields = ['number', 'number_year', 'address', 
        'applicant', 'object_name', 'research_kind']

    def get_context_data(self, **kwargs):
        context = super(ResearchEdit, self).get_context_data(**kwargs)
        context['header'] = u"Додавання експертного дослідження"
        return context

@method_decorator(login_required, name='dispatch')
class ResearchEdit(UpdateView):
    model = Research
    fields = ['number', 'number_year', 'address', 
        'applicant', 'object_name', 'research_kind', 'active']
    success_url = reverse_lazy('freports:researches_list')

    def get_context_data(self, **kwargs):
        context = super(ResearchEdit, self).get_context_data(**kwargs)
        context['header'] = u"Редагування експертного дослідження"
        return context


@method_decorator(login_required, name='dispatch')
class ResearchDelete(DeleteView):
    model = Research
    template_name = 'freports/delete_form.html'
    success_url = reverse_lazy('freports:researches_list')

    def get_context_data(self, **kwargs):
        context = super(ResearchDelete, self).get_context_data(**kwargs)
        context['header'] = u"Видалення експертного дослідження"
        context['content'] = u"Ви дійсно бажаєте видалити дослідження №{}".format(
            context['object'].full_number())
        return context

    def delete(self, request, *args, **kwargs):
        research = self.get_object()
        success_message = u"Дослідження {} успішно видалене!".format(
            research.full_number())
        messages.success(self.request, success_message)
        return super(ResearchDelete, self).delete(
            self, request, *args, **kwargs)