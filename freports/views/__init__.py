from .reports import reports_list, add_new_report_first, add_new_report, edit_report, delete_report, update_info
from .details import details_list, add_order, add_detail, edit_detail, delete_detail
from .participants import participants_list, participant_detail, add_participant, edit_participant, delete_participant
from .login import login_auth, logout_auth, login_attempts
from .contacts import contacts_list
from .subjects import subjects_list, subject_detail, add_subject, edit_subject, delete_subject
from .courts import courts_list, court_detail, add_court, edit_court, delete_court
from .judges import judges_list, judge_detail, add_judge, edit_judge, delete_judge
from .tasks import tasks_list, change_status_task, tasks_today_list, add_task, edit_task, delete_task
from .finances import accounts_list, add_account
