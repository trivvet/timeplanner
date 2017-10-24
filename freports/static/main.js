function initDateFields() {
    var defaultDate = $('input.dateinput').val(),
        calendarButton = "<i class='fa fa-calendar' aria-hidden='true'></i>";
    if (!defaultDate) {
        defaultDate = '2017-10-17'
    }
    $('input.dateinput').datepicker({
        autoclose: true,
        useCurrent: true,
        format: 'yyyy-mm-dd',
        viewDate: defaultDate,
        allowInputToggle: true,
        locale: 'uk',
        todayBtn: true,
    })

    $('.input-group-addon').click(function(){
        $(this).siblings('input').focus();
    });
}

function initRowMakeLink() {
    $('.td-link').click(function(){
        window.location = $(this).parent().data("href");
    });
}


$(document).ready(function(){
    initDateFields();
    initRowMakeLink();

})
