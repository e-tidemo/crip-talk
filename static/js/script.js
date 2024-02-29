//Confirm user is sure they want to delete
//
$(document).ready(function () {
    function showConfirmationModal(url, targetType) {
        $('#confirmationModal').modal('show');

        $('#confirmAction').on('click', function () {
            // Redirect to the delete URL
            window.location.href = url;
        });

        // Update the modal content based on the action type
        if (targetType === 'post') {
            $('#confirmationModalLabel').text('Delete Post');
            $('#confirmationMessage').text('Are you sure you want to delete this post?');
        } else if (targetType === 'comment') {
            $('#confirmationModalLabel').text('Delete Comment');
            $('#confirmationMessage').text('Are you sure you want to delete this comment?');
        }
    }

    // Attach click events to delete buttons
    $('.delete-post').on('click', function (e) {
        e.preventDefault();
        var deleteUrl = $(this).attr('href');
        showConfirmationModal(deleteUrl, 'post');
    });

    $('.delete-comment').on('click', function (e) {
        e.preventDefault();
        var deleteUrl = $(this).attr('href');
        showConfirmationModal(deleteUrl, 'comment');
    });
});