from .reports import (
    reports_list, 
    add_new_report, 
    report_edit, 
    delete_report, 
    update_info
    )
from .details import (
    details_list, 
    add_order, 
    add_detail, 
    edit_detail, 
    delete_detail,
    add_schedule,
    add_bill
    )
from .participants import (
    participants_list, 
    participant_detail, 
    add_participant, 
    edit_participant, 
    delete_participant
    )
from .contacts import (
    contacts_list, 
    contact_detail, 
    add_contact, 
    edit_contact, 
    delete_contact,
    update_contacts_status
    )
from .subjects import (
    subjects_list, 
    subject_detail, 
    add_subject, 
    edit_subject, 
    delete_subject
    )
from .courts import (
    courts_list, 
    court_detail, 
    add_court, 
    edit_court, 
    delete_court
    )
from .judges import (
    judges_list, 
    judge_detail, 
    add_judge, 
    edit_judge, 
    delete_judge
    )
from .tasks import (
    tasks_list, 
    change_status_task, 
    tasks_today_list, 
    add_task, 
    edit_task, 
    delete_task, 
    delete_old_tasks
    )

from .researches import (
    ResearchListView, 
    ResearchDetailView,
    add_new_research,
    ResearchCreate,
    ResearchEdit,
    ResearchDelete
    )
