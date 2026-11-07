document.addEventListener('DOMContentLoaded', () => {
    const navToggle = document.querySelector('.nav-dropdown-toggle');
    const navLinks = document.querySelector('.nav-links');

    if (navToggle && navLinks) {
        navToggle.addEventListener('click', (event) => {
            // Prevent click from immediately closing the menu if clicking inside
            event.stopPropagation(); 
            
            const isExpanded = navToggle.getAttribute('aria-expanded') === 'true';
            navToggle.setAttribute('aria-expanded', !isExpanded);
            navLinks.classList.toggle('active'); // Toggle visibility class
        });

        // Close dropdown if clicking outside of it
        document.addEventListener('click', (event) => {
            if (!navLinks.contains(event.target) && !navToggle.contains(event.target)) {
                if (navLinks.classList.contains('active')) {
                    navToggle.setAttribute('aria-expanded', 'false');
                    navLinks.classList.remove('active');
                }
            }
        });

        // Close dropdown on Escape key press
        document.addEventListener('keydown', (event) => {
            if (event.key === 'Escape' && navLinks.classList.contains('active')) {
                navToggle.setAttribute('aria-expanded', 'false');
                navLinks.classList.remove('active');
            }
        });

    } else {
        if (!navToggle) console.warn("Navigation dropdown toggle button not found.");
        if (!navLinks) console.warn("Navigation links container not found.");
    }
});
