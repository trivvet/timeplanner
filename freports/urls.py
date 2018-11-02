from django.conf.urls import url
from django.contrib import admin

from . import views

urlpatterns = [
    # report urls
    url(r'^$', views.reports_list, 
        name='reports_list'),
    url(r'^add/new_report/first/$', views.add_new_report_first, 
        name='add_new_report_first'),
    url(r'^add/new_report/$', views.add_new_report, 
        name='add_new_report'),
    url(r'^(?P<rid>\d+)/edit/$', views.edit_report, 
        name='edit_report'),
    url(r'^(?P<rid>\d+)/delete/$', views.delete_report, 
        name='delete_report'),
    url(r'^update_info/$', views.update_info, 
        name='reports_update'),

    # event urls
    url(r'^(?P<rid>\d+)/details/$', views.details_list, 
        name='report_detail'),
    url(r'^(?P<rid>\d+)/details/order/add/$', views.add_order, 
        name='add_order'),
    url(r'^(?P<rid>\d+)/details/add/(?P<kind>\w+)/$', 
        views.add_detail, name='add_detail'),
    url(r'^(?P<rid>\d+)/details/(?P<did>\d+)/edit/$', 
        views.edit_detail, name='edit_detail'),
    url(r'^(?P<rid>\d+)/details/(?P<did>\d+)/delete/$', 
        views.delete_detail, name='delete_detail'),

    # participant urls
    url(r'^partisipants/$', views.participants_list, 
        name='participants_list'),
    url(r'^partisipants/(?P<rid>\d+)/detail/$', 
        views.participant_detail, name='participant_detail'),
    url(r'^(?P<rid>\d+)/partisipants/add/(?P<status>\w+)/$', 
        views.add_participant, name='add_participant'),
    url(r'^(?P<rid>\d+)/partisipants/(?P<did>\d+)/edit/$', 
        views.edit_participant, name='edit_participant'),
    url(r'^(?P<rid>\d+)/partisipants/(?P<did>\d+)/delete/$', 
        views.delete_participant, name='delete_participant'),

    # subject urls
    url(r'^subjects/$', views.subjects_list, 
        name='subjects_list'),
    url(r'^subjects/(?P<sid>\d+)/detail/$', views.subject_detail, 
        name='subject_detail'),
    url(r'^(?P<rid>\d+)/subjects/add/$', views.add_subject, 
        name='add_subject'),
    url(r'^(?P<rid>\d+)/subjects/(?P<sid>\d+)/edit/$', 
        views.edit_subject, name='edit_subject'),
    url(r'^(?P<rid>\d+)/subjects/(?P<sid>\d+)/delete/$', 
        views.delete_subject, name='delete_subject'),

    # contact urls
    url(r'^contacts/$', views.contacts_list, name='contacts_list'),
    url(r'^contacts/(?P<cid>\d+)/detail/$', views.contact_detail, 
        name="contact_detail"),
    url(r'^contacts/add/$', views.add_contact, 
        name="add_contact"),
    url(r'^contacts/(?P<cid>\d+)/edit/$', views.edit_contact, 
        name="edit_contact"),
    url(r'^contacts/(?P<cid>\d+)/delete/$', views.delete_contact, 
        name="delete_contact"),

    # court urls
    url(r'^courts/$', views.courts_list, name='courts_list'),
    url(r'^courts/(?P<cid>\d+)/detail/$', views.court_detail, 
        name='court_detail'),
    url(r'^courts/add/$', views.add_court, 
        name='add_court'),
    url(r'^courts/(?P<cid>\d+)/edit/$', views.edit_court, 
        name='edit_court'),
    url(r'^courts/(?P<cid>\d+)/delete/$', views.delete_court, 
        name='delete_court'),

    # judge urls
    url(r'^judges/$', views.judges_list, name='judges_list'),
    url(r'^judges/(?P<jid>\d+)/detail/$', views.judge_detail, 
        name='judge_detail'),
    url(r'^judges/add/$', views.add_judge, 
        name='add_judge'),
    url(r'^judges/(?P<jid>\d+)/edit/$', views.edit_judge, 
        name='edit_judge'),
    url(r'^judges/(?P<jid>\d+)/delete/$', views.delete_judge, 
        name='delete_judge'),

    # task urls
    url(r'^tasks/$', views.tasks_list, name='tasks_list'),
    url(r'^tasks/change_status$', views.change_status_task, 
        name='change_status_task'),
    url(r'^tasks/today/$', views.tasks_today_list, 
        name='tasks_today_list'),
    url(r'^tasks/add/$', views.add_task, name='add_task'),
    url(r'^tasks/(?P<tid>\d+)/edit/$', views.edit_task, 
        name='edit_task'),
    url(r'^tasks/(?P<tid>\d+)/delete/$', views.delete_task, 
        name='delete_task'),
    url(r'^tasks/delete_old/$', views.delete_old_tasks, 
        name='delete_old'),
]