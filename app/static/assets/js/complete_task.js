// setInterval($.fn.get_count, 5000)
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
    $.fn.get_count();

    $(document).on('submit', 'form', function (event) {
        if($(this).hasClass('dynamic')){
            event.preventDefault();
        }


        if($(this).hasClass('dynamic')) {
            const formData = $(this).serialize();
            const form = this;
            const taskId = $(this).data('modal-task-id')
            const modal_view = '#modal-' + taskId;
            form.reset();

            $.ajax({
                type: 'POST',
                url: '/app/update_task/' + taskId,
                data: formData,
                success: function (response) {
                    $(modal_view).hide();
                    $('#Task-Holder').html(response);
                    $('body').removeClass('modal-open');
                    $('.modal-backdrop').remove();
                    $.fn.get_count();
                },
                error: function (error) {
                    console.error('Error:', error);
                }
            })

        }
    })

})