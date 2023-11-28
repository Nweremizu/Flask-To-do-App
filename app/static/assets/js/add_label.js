// Function to Get the Number of tasks and Numbers of Completed Tasks
$.fn.get_count = function () {
    $.ajax({
        type: 'GET',
        url: '/app/get_count',
        success: function (response) {
            $('#my_nav').html(response);
        },
        error: function (error) {

            console.error('Error:', error);
        }
    });
}


$(document).ready(function () {
    $.fn.get_count(); // Call the Get Count Function
    $('#label_form').submit(function (e) {
        $.fn.get_count();
        e.preventDefault();
        const formData = $(this).serialize();
        const form = this;
        form.reset();
        // Uses Ajax to call the add_label endpoint
        $.ajax({
            type: 'POST',
            url: '/app/add_label',
            data: formData,
            success: function (response) {
                if (response.message === 'Label added successfully'){
                    $.fn.get_count();
                    $('#list-modal').hide();
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                }
            },
            error: function (error) {
                console.error('Error', error);
            }
        })
    })
})