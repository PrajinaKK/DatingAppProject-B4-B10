document.addEventListener('DOMContentLoaded', function() {
    // Select all tabs and sections
    const tabs = document.querySelectorAll('.options-list-items');
    const sections = document.querySelectorAll('.section-content');

    // Add event listeners to each tab
    tabs.forEach(tab => {
        tab.addEventListener('click', function(event) {
            event.preventDefault();

            // Remove 'active' class from all tabs and 'd-none' class from all sections
            tabs.forEach(t => t.classList.remove('active'));
            sections.forEach(s => s.classList.add('d-none'));

            // Add 'active' class to the clicked tab
            tab.classList.add('active');

            // Show the section related to the clicked tab
            const targetId = tab.id.replace('-tab', '');
            const targetSection = document.getElementById(targetId);
            if (targetSection) {
                targetSection.classList.remove('d-none');
            }
        });
    });

    // Set the default active tab and section
    const defaultTab = document.getElementById('location-tab');
    if (defaultTab) {
        defaultTab.click();
    }
});
