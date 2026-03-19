/*
==========================================================================
NAV.JS
Hamburger toggle, dropdown accordion, outside tap to close.
Mobile: slides down from nav bar, auto height, sits over content.
Desktop: hover-activated dropdowns.
==========================================================================
*/

document.addEventListener('DOMContentLoaded', function () {
    const hamburger = document.getElementById('nav-hamburger');
    const navLinks = document.getElementById('nav-links');
    const dropdownTriggers = document.querySelectorAll('.nav-dropdown-trigger');

    // --- Hamburger toggle ---
    if (hamburger && navLinks) {
        hamburger.addEventListener('click', function (e) {
            e.stopPropagation();
            const isOpen = navLinks.classList.toggle('is-open');
            hamburger.classList.toggle('is-active', isOpen);
            hamburger.setAttribute('aria-expanded', isOpen.toString());
        });
    }

    // --- Dropdown toggles ---
    dropdownTriggers.forEach(function (trigger) {
        trigger.addEventListener('click', function (e) {
            e.stopPropagation();
            const parentItem = trigger.closest('.nav-item--dropdown');
            if (!parentItem) return;

            const isOpen = parentItem.classList.contains('is-open');

            // Close all other open dropdowns
            document.querySelectorAll('.nav-item--dropdown.is-open').forEach(function (item) {
                if (item !== parentItem) {
                    item.classList.remove('is-open');
                    const t = item.querySelector('.nav-dropdown-trigger');
                    if (t) t.setAttribute('aria-expanded', 'false');
                }
            });

            // Toggle this one
            parentItem.classList.toggle('is-open', !isOpen);
            trigger.setAttribute('aria-expanded', (!isOpen).toString());
        });
    });

    // --- Close on outside tap/click ---
    document.addEventListener('click', function (e) {
        if (!e.target.closest('.nav-item--dropdown')) {
            document.querySelectorAll('.nav-item--dropdown.is-open').forEach(function (item) {
                item.classList.remove('is-open');
                const t = item.querySelector('.nav-dropdown-trigger');
                if (t) t.setAttribute('aria-expanded', 'false');
            });
        }

        // Close mobile nav on outside tap
        if (navLinks && navLinks.classList.contains('is-open')) {
            if (!e.target.closest('.nav-container')) {
                navLinks.classList.remove('is-open');
                if (hamburger) {
                    hamburger.classList.remove('is-active');
                    hamburger.setAttribute('aria-expanded', 'false');
                }
            }
        }
    });

    // --- Close on Escape ---
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape') {
            if (navLinks) {
                navLinks.classList.remove('is-open');
                if (hamburger) {
                    hamburger.classList.remove('is-active');
                    hamburger.setAttribute('aria-expanded', 'false');
                }
            }
            document.querySelectorAll('.nav-item--dropdown.is-open').forEach(function (item) {
                item.classList.remove('is-open');
                const t = item.querySelector('.nav-dropdown-trigger');
                if (t) t.setAttribute('aria-expanded', 'false');
            });
        }
    });
});