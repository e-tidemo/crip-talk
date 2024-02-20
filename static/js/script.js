// Hover effect for dropdown navbar
document.getElementById('topicsDropdown').addEventListener('mouseenter', function () {
    new bootstrap.Dropdown(this.querySelector('.dropdown-toggle')).show();
});

document.getElementById('topicsDropdown').addEventListener('mouseleave', function () {
    new bootstrap.Dropdown(this.querySelector('.dropdown-toggle')).hide();
});

// Handle click to prevent navigation
document.getElementById('topicsDropdown').addEventListener('click', function (event) {
    event.preventDefault();
});
