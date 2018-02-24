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
from freports.admin import admin_site
from business_card import views as business_card

from axes.decorators import watch_login

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^myadmin/', admin_site.urls),

    # business card urls
    url(r'^$', business_card.first_page, name='business_card_first_page'),

    # report urls
    url(r'^freports/$', freports.reports_list, name='forensic_reports_list'),
    url(r'^freports/add/new_report/first/$', freports.add_new_report_first, name='forensic_add_new_report_first'),
    url(r'^freports/add/new_report/$', freports.add_new_report, name='forensic_add_new_report'),
    url(r'^freports/(?P<rid>\d+)/edit/$', freports.edit_report, name='forensic_edit_report'),
    url(r'^freports/(?P<rid>\d+)/delete/$', freports.delete_report, name='forensic_delete_report'),
    url(r'^freports/update_info/$', freports.update_info, name='reports_update'),

    # event urls
    url(r'^freports/(?P<rid>\d+)/details/$', freports.details_list, name='report_details_list'),
    url(r'^freports/(?P<rid>\d+)/details/order/add/$', freports.add_order, name='report_add_order'),
    url(r'^freports/(?P<rid>\d+)/details/add/(?P<kind>\w+)/$', freports.add_detail, name='report_add_detail'),
    url(r'^freports/(?P<rid>\d+)/details/(?P<did>\d+)/edit/$', freports.edit_detail, name='report_edit_detail'),
    url(r'^freports/(?P<rid>\d+)/details/(?P<did>\d+)/delete/$', freports.delete_detail, name='report_delete_detail'),

    # participant urls
    url(r'^freports/partisipants/$', freports.participants_list, name='forensic_participants_list'),
    url(r'^freports/partisipants/(?P<rid>\d+)/detail/$', freports.participant_detail, name='forensic_participant_detail'),
    url(r'^freports/(?P<rid>\d+)/partisipants/add/(?P<status>\w+)/$', freports.add_participant, name='report_add_participant'),
    url(r'^freports/(?P<rid>\d+)/partisipants/(?P<did>\d+)/edit/$', freports.edit_participant, name='report_edit_participant'),
    url(r'^freports/(?P<rid>\d+)/partisipants/(?P<did>\d+)/delete/$', freports.delete_participant,
        name='report_delete_participant'),

    # subject urls
    url(r'^freports/subjects/$', freports.subjects_list, name='report_subjects_list'),
    url(r'^freports/subjects/(?P<sid>\d+)/detail/$', freports.subject_detail, name='forensic_subject_detail'),
    url(r'^freports/(?P<rid>\d+)/subjects/add/$', freports.add_subject, name='report_add_subject'),
    url(r'^freports/(?P<rid>\d+)/subjects/(?P<sid>\d+)/edit/$', freports.edit_subject, name='report_edit_subject'),
    url(r'^freports/(?P<rid>\d+)/subjects/(?P<sid>\d+)/delete/$', freports.delete_subject,
        name='report_delete_subject'),

    # contact urls
    url(r'^contacts/$', freports.contacts_list, name='contacts_list'),

    # court urls
    url(r'^freports/courts/$', freports.courts_list, name='courts_list'),
    url(r'^freports/courts/(?P<cid>\d+)/detail/$', freports.court_detail, name='forensic_court_detail'),
    url(r'^freports/courts/add/$', freports.add_court, name='forensic_add_court'),
    url(r'^freports/courts/(?P<cid>\d+)/edit/$', freports.edit_court, name='forensic_edit_court'),
    url(r'^freports/courts/(?P<cid>\d+)/delete/$', freports.delete_court, name='forensic_delete_court'),

    # judge urls
    url(r'^judges/$', freports.judges_list, name='judges_list'),
    url(r'^freports/judges/(?P<jid>\d+)/detail/$', freports.judge_detail, name='forensic_judge_detail'),
    url(r'^freports/judges/add/$', freports.add_judge, name='forensic_add_judge'),
    url(r'^freports/judges/(?P<jid>\d+)/edit/$', freports.edit_judge, name='forensic_edit_judge'),
    url(r'^freports/judges/(?P<jid>\d+)/delete/$', freports.delete_judge, name='forensic_delete_judge'),

    # task urls
    url(r'^freports/tasks/$', freports.tasks_list, name='tasks_list'),
    url(r'^freports/tasks/add/$', freports.add_task, name='forensic_add_task'),
    url(r'^freports/tasks/(?P<tid>\d+)/edit/$', freports.edit_task, name='forensic_edit_task'),
    url(r'^freports/tasks/(?P<tid>\d+)/delete/$', freports.delete_task, name='forensic_delete_task'),

    url(r'^login/$', watch_login(freports.login_auth), name='login_form'),
    url(r'^logout/$', freports.logout_auth, name='logout_url'),
    url(r'^login/attempts/$', freports.login_attempts, name='login_attempts'),
]
