from django.conf.urls import url

from .views import (
    ReportListApiView, 
    ReportDetailApiView,
    ReportCreateAwardApiView
    )

urlpatterns = [
    # report urls
    url(r'^$', ReportListApiView.as_view(), 
        name='reports_list'),
    url(r'^(?P<pk>\d+)/$', ReportDetailApiView.as_view(),
        name='report_detail'),
    url(r'^create/$', ReportCreateAwardApiView.as_view(), 
        name='report_create')
]