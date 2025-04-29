document.addEventListener('DOMContentLoaded', function() {
    const sidebar = document.querySelector('#sidebar');
    const toggle = document.querySelector('.sidebar-toggle');

    if (!sidebar || !toggle) {
        console.error('Sidebar or toggle element not found');
        return;
    }

    // Mobile toggle
    toggle.addEventListener('click', function() {
        sidebar.classList.toggle('expanded');
        console.log('Sidebar toggled:', sidebar.classList.contains('expanded') ? 'Expanded' : 'Collapsed');
    });

    // Desktop hover
    sidebar.addEventListener('mouseenter', function() {
        sidebar.classList.add('expanded');
        console.log('Sidebar expanded on hover');
    });

    sidebar.addEventListener('mouseleave', function() {
        // Only collapse if not toggled open on mobile
        if (!toggle.offsetWidth) { // Check if toggle is hidden (desktop)
            sidebar.classList.remove('expanded');
            console.log('Sidebar collapsed on mouse leave');
        }
    });

    // Touch support for touch devices
    sidebar.addEventListener('touchstart', function(e) {
        e.preventDefault(); // Prevent default touch behavior
        sidebar.classList.toggle('expanded');
        console.log('Sidebar toggled on touch:', sidebar.classList.contains('expanded') ? 'Expanded' : 'Collapsed');
    });
});