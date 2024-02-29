// Function to set the modal content and action
function setConfirmationModal(title, message, confirmAction) {
    $('#confirmationModalLabel').text(title);
    $('#confirmationMessage').text(message);
    $('#confirmAction').data('action', confirmAction);
}

// When the delete button is clicked, set modal content and show the modal
$('.delete-post-button').click(function () {
    var title = 'Delete Post';
    var message = 'Are you sure you want to delete this post?';
    setConfirmationModal(title, message, 'delete-post');
    $('#confirmationModal').modal('show');
});

$('.delete-comment-button').click(function () {
    var title = 'Delete Comment';
    var message = 'Are you sure you want to delete this comment?';
    setConfirmationModal(title, message, 'delete-comment');
    $('#confirmationModal').modal('show');
});

// When the modal delete button is clicked, execute the appropriate action
$('#confirmAction').click(function () {
    var action = $('#confirmAction').data('action');
    if (action === 'delete-post') {
        // Execute delete post action
        $('#deletePostForm').submit();
    } else if (action === 'delete-comment') {
        // Execute delete comment action
        $('#deleteCommentForm').submit();
    }
});

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

// When the modal delete button is clicked, execute the appropriate action
$('#confirmAction').click(function () {
    var action = $('#confirmAction').data('action');
    if (action === 'delete-post') {
        // Execute delete post action
        $('#deletePostForm').submit();
    } else if (action === 'delete-comment') {
        // Execute delete comment action
        $('#deleteCommentForm').submit();
    }
});