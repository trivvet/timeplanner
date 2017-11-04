function initDateFields() {
    var startDate = $('input.dateinput').val(), currentDate = new Date(),
        calendarButton = "<i class='fa fa-calendar' aria-hidden='true'></i>";
    if (!startDate) {
        var startDate = currentDate;
    }
    $('input.dateinput').datetimepicker({
      format: 'YYYY-MM-DD',
      icons: {
          date: "fa fa-calendar",
          previous: "fa fa-arrow-left",
          next: "fa fa-arrow-right",
          close: 'fa fa-times',
          today: 'fa fa-calendar-check-o'
      },
      locale: 'uk',
      maxDate: currentDate,
      viewDate: startDate,
      defaultDate: startDate,
      useCurrent: false,
      daysOfWeekDisabled: [0,6]
    });

//    $('.input-group-addon').click(function(){
//        $(this).siblings('input').focus();
//    });
}

function initDateTimeFields() {
    $('input.datetimeinput').datetimepicker({
      format: 'YYYY-MM-DD HH:mm',
      icons: {
          time: "fa fa-clock-o",
          date: "fa fa-calendar",
          up: "fa fa-arrow-up",
          down: "fa fa-arrow-down",
          previous: "fa fa-arrow-left",
          next: "fa fa-arrow-right",
          close: 'fa fa-times',
          today: 'fa fa-calendar-check-o'
      },
      sideBySide: true,
      stepping: 30,
      locale: 'uk',
      daysOfWeekDisabled: [0,6]
    });
}

function initRowMakeLink() {
    $('.td-link').click(function(){
        window.location = $(this).parent().data("href");
    });
}

function initFormPage() {
    $('#add-event>a, #edit-event a').click(function() {
        var link = $(this);

        $.ajax({
            'url': link.attr('href'),
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
                var modal = $('#modalForm'), html = $(data), form = html.find('#main-content form');
                modal.find('#first-header').html(html.find('#second-header h2')).val();
                modal.find('.modal-body').html(form);
                modal.find('.modal-body').prepend(html.find('#second-header .row'));

                initForm(form, modal, link.attr('href'));

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

function initForm(form, modal, link) {
    initDateFields();
    initDateTimeFields();

    form.ajaxForm({
        url: link,
        dataType: 'html',
        error: function() {
            alert("Вибачте, але на сервері сталася неочікувана помилка. Перезавантажте сторінку та спробуйте ще раз");
            return false;
        },
        success: function(data, status, xhr) {
            var html = $(data), newform = html.find('#main-content form');

            if (newform.length > 0) {
                modal.find('.modal-body').html(newform);
                modal.find('.modal-body').prepend(html.find('.alert'));
                modal.find('.modal-body').prepend(html.find('#second-header h3'));
                initForm(newform, modal, link);
            } else {
                $('#message .col').html(html.find('.alert'));
                $('#main-content').html(html.find('#main-content').html());
                initFormPage();
                $('#modalForm').modal('hide');
            }
        }
    });
}

$(document).ready(function(){
    initDateFields();
    initDateTimeFields();
    initRowMakeLink();
    initFormPage();

})
