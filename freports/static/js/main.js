function initDateFields() {
    var startDate = $('#inputDate input').val(), currentDate = new Date();
    if (!startDate) {
        var startDate = currentDate;
    }
    // $('#inputDateDecision').parent().hide();
    $('#inputDate').datetimepicker({
        format: 'YYYY-MM-DD',
        locale: 'uk',
        date: startDate,
        maxDate: currentDate,
        defaultDate: startDate,
        useCurrent: false,
        daysOfWeekDisabled: [0],
        buttons: {
            showToday: true,
            showClose: true
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
    var startDate = $('#datetimepicker1 input').val(), currentDate = new Date();
    if (!startDate) {
        var startDate = currentDate;
    }
    $('#datetimepicker1').datetimepicker({
        format: 'YYYY-MM-DD HH:mm',
        sideBySide: true,
        locale: 'uk',
        date: startDate,
        stepping: 30,
        useCurrent: false,
        daysOfWeekDisabled: [0,7],
        minDate: startDate,
        enabledHours: [7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22]
    });
}

function initChangeDecisionDate() {
    $('#inputDate').focusout(function() {
        // $('#inputDateDecision').parent().show();
        var inputDate = $('#inputDateDecision');
        if (inputDate) {
            var inputDateValue = new Date(inputDate.children('input').val());
            var eventDate = new Date($(this).children('input').val());
            var maxDate = new Date($(this).children('input').val());
            if (inputDateValue > eventDate || maxDate > eventDate) {
                eventDate.setDate(eventDate.getDate() - 10);
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
    initDateTimeFields();
    initDateDecisionField();
    initSelectCourt(link);

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
                $('#message .col').html(html.find('.alert'));
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

function inputNumberField() {
    $('#inputCase').focus(function() {
        current_value = $(this).val();
        if (current_value.includes('/17') || current_value.includes('/16')) {
            end_of_array = current_value.indexOf('/', 5);
            $(this).get(0).setSelectionRange(4,end_of_array);
        } else {
            $('#inputCase').val(current_value + ' /17');
            $(this).get(0).setSelectionRange(4,5);
        }
    });
}

function addPlusButton() {
    $('.report-detail-item').parent().parent().mouseenter(function() {
        $(this).find('.btn-outline-success').removeAttr('hidden');
        $(this).mouseleave(function() {
            $(this).find('.btn-outline-success').attr('hidden', '1');
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
        var box = $(this);
        if (box.val()) {
            var taskKey = box.val();
        } else {
            var taskKey = box.data('pk');
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
                taskLine = box.parents('tr');
                content = "<td colspan='6'>Завдання виконане</td>";
                if (data.next_url) {
                    activateModalPage(data.next_url);
                }
                taskLine.removeClass('table-danger').addClass('table-success text-center').html(content);
                taskLine.fadeOut(1500, function() {
                    $(this).remove();
                });
            }
        });
    });
}

function showSidebar() {
    if ($.cookie("sidebar")) {
        $('#sidebar').addClass('active');
        $('#sidebarCollapse').addClass('active');
    } else {
        $('#sidebar').removeClass('active');
        $('#sidebarCollapse').removeClass('active');
    }
    $('#sidebarCollapse').on('click', function() {
        $('#sidebar').toggleClass('active');
        $(this).toggleClass('active');
        if ($('#sidebar').hasClass('active')) {
            $.cookie("sidebar", 'active');
        } else {
            $.removeCookie('sidebar');
        }
    })
}

$(document).ready(function(){
    initDateFields();
    initDateTimeFields();
    initRowMakeLink();
    initTodayTasksPage()
    initFormPage();
    initSelectCourt();
    addPlusButton();
    showButtons();
    clickExecuteTask();
    showSidebar();
})
