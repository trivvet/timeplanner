"""timeplanner URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin

from freports import views as freports

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    url(r'^$', freports.reports_list, name='forensic_reports_list'),
    url(r'^freports/add/report/$', freports.add_report, name='forensic_add_report'),
    url(r'^freports/(?P<rid>\d+)/edit/$', freports.edit_report, name='forensic_edit_report'),
    url(r'^freports/(?P<rid>\d+)/delete/$', freports.delete_report, name='forensic_delete_report'),

    url(r'^freports/(?P<rid>\d+)/details/$', freports.details_list, name='report_details_list'),
    url(r'^freports/(?P<rid>\d+)/details/add/$', freports.add_detail, name='report_add_detail'),
    url(r'^freports/(?P<rid>\d+)/details/(?P<did>\d+)/edit/$', freports.edit_detail, name='report_edit_detail'),
    url(r'^freports/(?P<rid>\d+)/details/(?P<did>\d+)/delete/$', freports.delete_detail, name='report_delete_detail'),

    url(r'^partisipants/$', freports.participants_list, name='forensic_participants_list'),
    url(r'^partisipants/(?P<rid>\d+)/detail/$', freports.participant_detail, name='forensic_participant_detail'),
    url(r'^freports/(?P<rid>\d+)/partisipants/add/$', freports.add_participant, name='report_add_participant'),
    url(r'^freports/(?P<rid>\d+)/partisipants/(?P<did>\d+)/edit/$', freports.edit_participant, name='report_edit_participant'),
    url(r'^freports/(?P<rid>\d+)/partisipants/(?P<did>\d+)/delete/$', freports.delete_participant,
        name='report_delete_participant'),

    url(r'^contacts/$', freports.contacts_list, name='contacts_list'),

    url(r'^login/$', freports.login_auth, name='login_form'),
    url(r'^logout/$', freports.logout_auth, name='logout_url'),
]
