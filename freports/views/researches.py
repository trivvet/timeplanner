from django.utils import timezone
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView

from ..models import Research

class ResearchListView(ListView):

    model = Research
    paginate_by = 10  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super(ResearchListView, self).get_context_data(**kwargs)
        # context['now'] = timezone.now()
        return context


class ResearchCreate(CreateView):

    model = Research
    fields = ['number', 'number_year', 'address', 
        'applicant', 'object_name', 'research_kind']