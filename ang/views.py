import os

from django.conf import settings
from django.http import HttpResponse, Http404
from django.views import View

class AngularTemplateView(View):
    def get(self, request, item='report-list', *args, **kwargs):
        template_dir_path = settings.TEMPLATES[0]["DIRS"][0]
        final_path = os.path.join(template_dir_path, "ang",
            item + '.html')
        print final_path
        try:
            html = open(final_path)
            return HttpResponse(html)
        except:
            raise Http404