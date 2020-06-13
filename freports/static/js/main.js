// init datetimepicker for input with date format
function initDateFields() {
    $('#inputDate, #inputDate2').attr('autocomplete', 'off');
    var startDate = $('#inputDate input').val(), 
        currentDate = moment(),
        startDateOne = $('#inputDate').val(),
        startDate3 = $('#inputDate3').val();
    var maxDate = moment().millisecond(0).second(0).minute(0).hour(0);
    maxDate.add(23, 'h');
    if (!startDate && !startDateOne) {
        var startDate = currentDate;
    } else if (startDateOne) {
        var startDate =startDateOne;
    }
    var startDate2 = $('#inputDate2').val();
    if (!startDate2) {
        if (startDateOne) {
            startDate2 = startDateOne;
        } else {
            startDate2 = startDate
        }
    }
    $('#inputDate, #inputDate3').datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'uk',
        date: startDate3,
        maxDate: maxDate,
        defaultDate: startDate,
        useCurrent: false,
        daysOfWeekDisabled: [0],
        buttons: {
            showToday: true,
            showClose: true
        }
    });
    $('#inputDate2').datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'uk',
        date: startDate2,
        maxDate: currentDate,
        defaultDate: startDate2,
        useCurrent: false,
        daysOfWeekDisabled: [0],
        buttons: {
            showToday: true,
            showClose: true
        }
    });
    $('#inputDate, #inputDate2, #inputDate3').on("blur", function(e) {
        $(this).off("focus").datetimepicker('hide');
    });
}

function showExecutedDate() {
    var status = $("#id_id_status_0_3").is(":checked");
    if (!status) {
        $("#div_id_date_executed").hide();
    }
    $('#div_id_status input:radio').on("click", function() {
        if (this.value == "done") {
            $("#div_id_date_executed").show();
        } else {
            $("#div_id_date_executed").hide();
        }
    });
}

function initDateDecisionField() {
    var maxDate = $('#inputDate input').val(), currentDate = new Date();
    if (!maxDate) {
        maxDate = currentDate;
    }
    $('#inputDateDecision').datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'uk',
        maxDate: maxDate,
        useCurrent: false,
        daysOfWeekDisabled: [0,6]
    });
    initChangeDecisionDate();
}

function initDateTimeFields() {
    var startDate = $('#datetimepicker1 input').val(), 
        inputDate = $('#inputDate input').val(),
        minDate = new Date();
    if (!startDate && inputDate) {
        minDate = new Date(inputDate);
        minDate.setHours(15);
        startDate = minDate;
    } else if (startDate) {
        startDate = new Date(startDate);
        minDate = new Date(startDate);
        minDate.setHours(8);
    } else {
        startDate = new Date();
        startDate.setHours(startDate.getHours() + 1)
    }
    $('#datetimepicker1').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        sideBySide: true,
        locale: 'uk',
        date: startDate,
        stepping: 30,
        useCurrent: false,
        daysOfWeekDisabled: [0,7],
        minDate: minDate,
        enabledHours: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    });
}

function initChangeDecisionDate() {
    $('#inputDate').focusout(function() {
        var inputDate = $('#inputDateDecision');
        if (inputDate) {
            var inputDateValue = new Date(inputDate.children('input').val());
            var eventDate = new Date($(this).children('input').val());
            var maxDate = new Date($(this).children('input').val());
            eventDate.setDate(eventDate.getDate() - 21);
            if (inputDateValue > eventDate || maxDate > eventDate) {
                inputDate.datetimepicker('destroy');
                $('#inputDateDecision').datetimepicker({
                    format: 'YYYY-MM-DD',
                    locale: 'uk',
                    date: eventDate,
                    maxDate: maxDate,
                    useCurrent: false,
                    daysOfWeekDisabled: [0,6]
                });
            } else if (!inputDateValue) {
                inputDate.datetimepicker('destroy');
                $('#inputDateDecision').datetimepicker({
                    format: 'YYYY-MM-DD',
                    locale: 'uk',
                    date: eventDate,
                    maxDate: maxDate,
                    useCurrent: false,
                    daysOfWeekDisabled: [0,6]
                });
            }
        } 
        
    }).blur();
}

function initChangeScheduleDate() {
    $('#inputDate').focusout(function() {
        if ($('#inputDateSchedule').length) {
            var inputDate = $('#inputDateSchedule');
            if (inputDate) {
                var eventDate = new Date($(this).children('input').val());
                eventDate.setDate(eventDate.getDate() + 10);
                eventDate.setHours(15);
                inputDate.parent().datetimepicker('destroy');
                $('#datetimepicker1').datetimepicker({
                    format: 'YYYY-MM-DD HH:mm',
                    sideBySide: true,
                    locale: 'uk',
                    date: eventDate,
                    stepping: 30,
                    useCurrent: false,
                    daysOfWeekDisabled: [0,7],
                    minDate: eventDate,
                    enabledHours: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
                });
            }
        }   
    });
}

function initTodayTasksPage() {
    $('#btnGroupDrop1').click(function() {
        var link = $(this);

        $.ajax({
            'url': link.attr('href'),
            'dataType': 'html',
            'type': 'get',
            'beforeSend': function() {
                // $('.dropdown-menu').removeClass('show');
                // $('.dropdown').removeClass('show');
            },
            'success': function(data, status, xhr) {
                if (status != 'success') {
                    alert("Вибачте, але на сервері сталася неочікувана помилка. Перезавантажте сторінку та спробуйте ще раз");
                    return false;
                }
                var modal = $('#modalForm'), html = $(data);
                modal.find('#first-header div').html(html.find('#task-list-header'));
                modal.find('.modal-body').html(html.find('table'));
                modal.find('.modal-body').prepend(html.find('.tasks_free'));
                modal.find('.modal-footer').html(html.find('#add-report'))

                showButtons();
                initFormPage()

                $('#modalForm').modal({'show': true});
            },
            'error': function() {
                alert('Error on the server');
                return false;
            }
        });

        return false
    });
}

function initRowMakeLink() {
    $('.td-link').click(function(){
        row = $(this).parent()
        if(row.hasClass('table-danger')) {
            activateModalPage(row.data("href"));
        } else {
            window.location = row.data("href");
        }
    });
}

function initFormPage() {
    $('.modal-button').on("click", function() {
        activateModalPage($(this).attr('href'));
        return false
    });
}

function activateModalPage(link) {
    $.ajax({
        'url': link,
        'dataType': 'html',
        'type': 'get',
        'beforeSend': function() {
            $('.dropdown-menu').removeClass('show');
            $('.dropdown').removeClass('show');
        },
        'success': function(data, status, xhr) {
            if (status != 'success') {
                alert("Вибачте, але на сервері сталася неочікувана помилка. Перезавантажте сторінку та спробуйте ще раз");
                return false;
            }
            if (data.length < 100) {
                var data_info = JSON.parse(data);
                if (data_info.modal == 'false') {
                    location.reload();
                }
            }
            var modal = $('#modalForm'), html = $(data), form = html.find('#main-content form');
            modal.find('#first-header div').html(html.find('#second-header h2'));
            modal.find('.modal-body').html(form);
            modal.find('.modal-body').prepend(html.find('#second-header .row'));

            initForm(form, modal, link);

            $('#modalForm').modal({'show': true});
        },
        'error': function(error) {
            alert('Error on the server: ' + error.status);
            return false;
        }
    });
}

function initForm(form, modal, link) {
    initDateFields();
    showExecutedDate()
    initDateTimeFields();
    initDateDecisionField();
    initSelectCourt(link);
    closeModalForm();
    initGetOrderValues(link);
    showParticipantMessageType()
    initChangeScheduleDate();
    initSelectPetitionType();

    form.ajaxForm({
        url: link,
        dataType: 'html',
        error: function() {
            alert("Вибачте, але на сервері сталася неочікувана помилка. Перезавантажте сторінку та спробуйте ще раз");
            return false;
        },
        success: function(data, status, xhr) {
            var html = $(data), newform = html.find('#main-content form.form-horizontal');

            if (newform.length > 0) {
                modal.find('.modal-body').html(newform);
                modal.find('.modal-body').prepend(html.find('.alert'));
                modal.find('.modal-body').prepend(html.find('#second-header h3'));
                initForm(newform, modal, link);
            } else {
                $('#navbarSupportedContent').html(html.find('#navbarSupportedContent'));
                $('#message .col').html(html.find('.alert'));
                $('#second-header').html(html.find('#second-header').html());
                $('#main-content').html(html.find('#main-content').html());
                $('#extra-content').html(html.find('#extra-content').html());
                initFormPage();
                addPlusButton();
                initRowMakeLink();
                showButtons();
                clickExecuteTask();
                $('#modalForm').modal('hide');
            }
        }
    });
}

function closeModalForm() {
    $('#button-id-submit').on("click", function() {
        $('#modalForm').modal('hide');
    });
}

function initSelectCourt(link) {
    $('#inputCourtForOrder').change(function() {
        $.ajax('', {
            'url': link,
            'type': 'GET',
            'async': true,
            'dataType': 'json',
            'data': {'court': $(this).val()},
            'error': function(xhr, status, error) {
                alert(error);
            },
            'success': function(data, status, xhr) {
                $('#inputJudge').parent().parent().removeAttr('hidden');
                $('#inputJudge').html('<option value="">-----</option>');
                for (i=0, len=data.judges.length; i<len; i++) {
                    option = '<option value=' + data.judges[i].id + '>' + data.judges[i].short_name + '</option>'
                    $('#inputJudge').append(option);
                }
                if (data.court_number) {
                    case_number = data.court_number + '/';
                    $('#inputCase').val(case_number);
                    inputNumberField();
                }
            },
        });
    });
    if ($('#inputCourtForOrder').val()) {
        inputNumberField();
    }
}

function initSelectPetitionType() {
    $('#inputType').change(function() {
        var textArea = $('#inputNecessary')
        if ($(this).val() == "Про надання справи") {
            textArea.val('Необхідно надати матеріали справи для ознайомлення');
            textArea.attr('readonly', true);
        } else if ($(this).val() == "Про уточнення питань") {
            textArea.val('Необхідно уточнити поставлені на вирішення експертизи питання, а саме: ');
            textArea.attr('readonly', false);
        } else if ($(this).val() == "Про надання додаткових матеріалів") {
            textArea.val('Необхідно надати додаткові матеріали, а саме: ');
            textArea.attr('readonly', false);
        }
    });
}

function initGetOrderValues(link) {
    $('#id_order').change(function() {
        if ($(this).val()) {
            $.ajax('', {
                'url': link,
                'type': 'GET',
                'async': true,
                'dataType': 'json',
                'data': {'order_id': $(this).val(), 'format': 'json'},
                'error': function(xhr, status, error) {
                    alert(error);
                },
                'success': function(data, status, xhr) {
                    $('#id_amount').val(data.total_sum);
                    $('#id_account').val(data.account_id);
                    $('#id_closed_tasks').val(data.tasks_number);
                },
            });
        } else {
            $('#id_amount').val("");
        }
        
    });
}


// Спрацьовує на формі додавання провадження в полі номеру справи
function inputNumberField() {
    $('#inputCase').focus(function() {
        current_value = $(this).val();
        is_current = false;
        for (i=12; i<20; i++) {
            is_current = current_value.includes('/' + i);
            if (is_current) {
                break
            }
        }
        if (is_current) {
            end_of_array = current_value.indexOf('/', 5);
            $(this).get(0).setSelectionRange(4,end_of_array);
        } else {
            $('#inputCase').val(current_value + ' /19');
            $(this).get(0).setSelectionRange(4,5);
        }
    });
}


function addPlusButton() {
    $('.report-detail-item').parent().parent().mouseenter(function() {
        $(this).find('.btn-outline-success, .btn-outline-info').removeAttr('hidden');
        $(this).mouseleave(function() {
            $(this).find('.btn-outline-success, .btn-outline-info').attr('hidden', '1');
        });
    });
}


function showButtons() {
    $('tbody tr').hover(function() {
        $(this).find(".fa").fadeIn(100);
    }, function() {
        $(this).find(".fa").fadeOut(100);
    });
}


function clickExecuteTask() {
    $('.checkbox-container input, .try').click(function() {
        var box = $(this), taskKey = "";
        if (box.val()) {
            taskKey = box.val();
        } else {
            taskKey = box.data('pk');
        }
        $.ajax(box.data('url'), {
            'type': 'POST',
            'async': true,
            'dataType': 'json',
            'data': {
                'pk': taskKey,
                'csrfmiddlewaretoken': $('input[name="csrfmiddlewaretoken"]').val()
            },
            'beforeSend': function(xhr, setting) {
                box.prop('disabled', true);
            },
            'error': function(xhr, status, error) {
                alert(error);
            },
            'success': function(data, status, xhr) {
                var taskLine = box.parents('tr.task-line'),
                    activeTasksList = box.parents('#active-tasks-list'),
                    content = "<td colspan='6'>Завдання виконане</td>",
                    taskSiblings = '';

                if(!taskLine.length) {
                    taskLine = box.parents('li.list-group-item');
                    var taskSiblings = taskLine.siblings();
                    content = "Завдання виконане";
                }

                if (data.next_url) {
                    activateModalPage(data.next_url);
                }
                taskLine.removeClass('table-danger').
                    addClass('table-success text-center').html(content);
                taskLine.fadeOut(1500, function() {
                    $(this).remove();
                });
                if(taskSiblings.length == 1) {
                    activeTasksList.fadeOut(1500, function() {
                        $(this).remove();
                    });
                }
            }
        });
    });
}

function showSidebar() {
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
        if ($('#sidebar').hasClass('active')) {
            $.cookie("sidebar", 'active', {path: '/'});
        } else {
            $.cookie("sidebar", 'inactive', {path: '/'});
        }
    });
}

function clickFilterButton() {
    if ($('#filter')) {
        initDateFields();
    }
}

// Show select when click checkbox on schedule add form
function showParticipantMessageType() {
    $('input.person-сheckbox').on('change', function() {
        inputSelect = $(this).next().children('select')
        if($(this).is(':checked')) {
            inputSelect.removeClass('d-none').removeAttr('disabled');
            initMessageSelect(inputSelect);
            $('input[name=save_button]').attr('disabled', true);
        } else {
            $(this).next().children().each(function() {
                $(this).addClass('d-none').attr('disabled', true);
            });
            $('input[name=save_button]').removeAttr('disabled');
        }
    });
}

// Show inputs when choose type message on schedule add form
function initMessageSelect(select) {
    select.children().first().attr('disabled', true);
    select.on('change', function() {
        if ($(this).val() == 'letter') {
            select.siblings().each(function(input) {
                $(this).addClass('d-none').attr('disabled', true);
            });
            select.siblings("[id='address-input']").removeClass(
                'd-none').removeAttr('disabled');
            select.siblings("[name='letter']").removeClass(
                'd-none').removeAttr('disabled');
        } else if($(this).val() == 'call' || $(this).val() == 'viber') {
            select.siblings().each(function() {
                $(this).addClass('d-none').attr('disabled', true);
            });
            select.siblings("[id='phone-input']").removeClass(
                'd-none').removeAttr('disabled');
        } else if ($(this).val() == 'agent') {
            select.siblings().each(function(input) {
                $(this).addClass('d-none').attr('disabled', true);
            });
            select.siblings("[id='agent-input']").removeClass(
                'd-none').removeAttr('disabled');
        }
        $('input[name=save_button]').removeAttr('disabled');
    });
}

$(document).ready(function(){
    // initDateFields();
    initDateTimeFields();
    initRowMakeLink();
    initTodayTasksPage()
    initFormPage();
    initSelectCourt();
    addPlusButton();
    showButtons();
    clickExecuteTask();
    showSidebar();
    clickFilterButton();
})
