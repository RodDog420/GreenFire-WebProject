/*
==========================================================================
AGE-GATE.JS
Always checks for cookie on page load.
If cookie gf_age_verified exists, removes gate immediately.
If not, gate stays visible until user confirms.
Cookie expires after 1 year — user never sees gate again on same device.
==========================================================================
*/

(function () {
    // Check cookie on page load — remove gate instantly if already verified
    function getCookie(name) {
        const value = '; ' + document.cookie;
        const parts = value.split('; ' + name + '=');
        if (parts.length === 2) return parts.pop().split(';').shift();
        return null;
    }

    const gate = document.getElementById('age-gate');

    if (getCookie('gf_age_verified') === 'true') {
        // Already verified — remove gate immediately, no flash
        if (gate) gate.remove();
    }
})();


function ageGateConfirm() {
    // Set cookie — expires in 1 year
    const expires = new Date();
    expires.setFullYear(expires.getFullYear() + 1);
    document.cookie = 'gf_age_verified=true; expires=' + expires.toUTCString() + '; path=/; SameSite=Lax';

    const gate = document.getElementById('age-gate');
    if (gate) {
        gate.style.opacity = '0';
        gate.style.transition = 'opacity 0.3s ease';
        setTimeout(() => gate.remove(), 300);
    }
}

function ageGateDeny() {
    window.location.href = 'https://www.google.com';
}