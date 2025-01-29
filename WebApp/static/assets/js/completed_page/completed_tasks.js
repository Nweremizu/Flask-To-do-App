
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
    // all checkbox should be always check and should be unable to be unchecked
    $('.form-check-input').prop('checked', true);
    $('.form-check-input').prop('disabled', true);



    $('.btn-success').click(function (event) {
        event.preventDefault();
        const taskId = $(this).data('id');
        console.log(taskId)
        const modal_view = '#modal-' + taskId;
        const task_select = '#com-' + taskId;

        $.ajax({
            type: 'POST',
            url: '/app/restore_task/' + taskId,
            data: {
                'csrf_token': $('input[name=csrf_token]').val()
            },
            success: function (response) {

                if (response.message === 'Task restored successfully') {
                    console.log(response.message)
                    $.ajax({
                        type: 'GET',
                        url: '/app/new_completed_tasks',
                        success: function (get_response) {
                            $(modal_view).hide();
                            $('#Task-Holder').html(get_response);
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            $.fn.get_count();
                        },
                        error: function (error) {
                            console.error('Error:', error);
                        }
                    })
                }
            },
            error: function (error2) {
                console.error('Error:', error2);
            }
        })
    })


    $('.btn-danger').click(function (event) {
        event.preventDefault();
        const taskId = $(this).data('id');
        console.log(taskId)
        const modal_view = '#modal-' + taskId;
        const task_select = '#com-' + taskId;

        $.ajax({
            type: 'POST',
            url: '/app/delete_task/' + taskId,
            data: {
                'csrf_token': $('input[name=csrf_token]').val()
            },
            success: function (del_response) {

                if (del_response.message === 'Task deleted successfully') {
                    console.log(del_response.message)
                    $.ajax({
                        type: 'GET',
                        url: '/app/new_completed_tasks',
                        success: function (get_response) {
                            $(modal_view).hide();
                            $('#Task-Holder').html(get_response);
                            $('body').removeClass('modal-open');
                            $('.modal-backdrop').remove();
                            $.fn.get_count();
                        },
                        error: function (error) {
                            console.error('Error:', error);
                        }
                    })
                }
            },
            error: function (error2) {
                console.error('Error:', error2);
            }
        })
    })
})