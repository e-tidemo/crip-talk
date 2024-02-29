// Function to set the modal content and action
function setConfirmationModal(title, message, confirmAction) {
    $('#confirmationModalLabel').text(title);
    $('#confirmationMessage').text(message);
    $('#confirmAction').data('action', confirmAction);
}

// When the delete button is clicked, set modal content and show the modal
$('.delete-post-button').click(function (e) {
    e.preventDefault(); // Prevent the default action of the button
    var title = 'Delete Post';
    var message = 'Are you sure you want to delete this post?';
    setConfirmationModal(title, message, 'delete-post');
    $('#confirmationModal').modal('show');
});

$('.delete-comment-button').click(function (e) {
    e.preventDefault(); // Prevent the default action of the button
    var title = 'Delete Comment';
    var message = 'Are you sure you want to delete this comment?';
    setConfirmationModal(title, message, 'delete-comment');
    $('#confirmationModal').modal('show');
});

// Update the modal action and submit the form when the "Delete" button is clicked
$('#confirmAction').click(function () {
    var action = $('#confirmAction').data('action');
    if (action === 'delete-post') {
        // Update the form action
        $('#deletePostForm').attr('action', '/delete-post/' + post.slug + '/');
        // Submit the form
        $('#deletePostForm').submit();
    } else if (action === 'delete-comment') {
        // Update the form action
        $('#deleteCommentForm').attr('action', '/delete-comment/' + comment.id + '/');
        // Submit the form
        $('#deleteCommentForm').submit();
    }
});
