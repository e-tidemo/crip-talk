<script>
    // Hover effect for dropdown navbar
    document.getElementById('topicsDropdown').addEventListener('mouseenter', function () {
        this.querySelector('.dropdown-menu').classList.add('show') 
        });

    document.getElementById('topicsDropdown').addEventListener('mouseleave', function () {
        this.querySelector('.dropdown-menu').classList.remove('show') 
        });
</script>