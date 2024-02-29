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
    var postId = $(this).data('post-id');
    setConfirmationModal(title, message, 'delete-post', postId);
    $('#confirmationModal').modal('show');
});

$('.delete-comment-button').click(function (e) {
    e.preventDefault(); // Prevent the default action of the button
    var title = 'Delete Comment';
    var message = 'Are you sure you want to delete this comment?';
    var commentId = $(this).data('comment-id'); // Fetch the comment id from data attribute
    setConfirmationModal(title, message, 'delete-comment', commentId);
    $('#confirmationModal').modal('show');
});

// Update the modal action and submit the form when the "Delete" button is clicked
$('#confirmAction').click(function () {
    var action = $('#confirmAction').data('action');
    if (action === 'delete-post') {
        $('#deletePostForm').attr('action', '/delete-post/' + post.slug + '/');
        $('#deletePostForm').submit();
    } else if (action === 'delete-comment') {
        $('#deleteCommentForm').attr('action', '/delete-comment/' + $('#confirmAction').data('comment-id') + '/');
        $('#deleteCommentForm').submit();
    }
});
