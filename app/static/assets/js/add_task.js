$('.form-check-input').prop('checked', false);
$('#add_task').val('');

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
    $('.addTask').click(function () {
        $('#add_task').focus();
    })
    
    $('#AddTaskForm').submit(function (event) {
        event.preventDefault(); // Prevent the default form submission

        const formData = $(this).serialize(); // Serialize the form data
        const form = this; // Store a reference to the form element
        form.reset();

        $.ajax({
            type: 'POST',
            url: '/app/add_task', // Use Flask URL routing here
            data: formData,
            success: function (response) {
                $.fn.get_count();
                // Smooth animation effect
                $('#Task-Holder').fadeOut(1000, function () {
                    // Update the content and fadeIn
                    $(this).html(response).fadeIn(1000);

                    // Reset the form after submission
                    form.reset();
                });
            },
            error: function (error) {
                console.error('Error:', error);
            }
        });
    });

    // Handle Enter key press in the input field
    $('#add_task').keydown(function (event) {
        if (event.keyCode === 13) { // Check if the Enter key (key code 13) is pressed
            event.preventDefault();
            $('#AddTaskForm').submit(); // Trigger the form submission
        }
    });

    // Handle The completion of the tasks
    $('.form-check-input').change(function () {
        if ($(this).is(':checked')) {
            const taskId = $(this).data('task-id');
            console.log(taskId);
            const $this = $(this);
            const modal = '#modal-' + taskId;
            $.ajax({
                type: 'POST',
                url: '/app/complete_task/' + taskId,
                headers: {
                    'X-CSRFToken': $('#crsf').val() // Retrieve the CSRF token value
                },
                success: function (response) {
                    if (response.message === 'Task completed successfully') {
                        $.fn.get_count();
                        // Use $this instead of $(this) inside the callback function
                        $this.closest('.task-item').fadeOut(600, function () {
                            $(this).remove();
                        });
                        $(modal).remove();
                    }
                },

            });
        }
    });


    // when the mark-done icon is clicked it performs same completion


});



