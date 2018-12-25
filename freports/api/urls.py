from django.conf.urls import url

from .views import ReportListApiView

urlpatterns = [
    # report urls
    url(r'^$', ReportListApiView.as_view(), 
        name='reports_list'),
]