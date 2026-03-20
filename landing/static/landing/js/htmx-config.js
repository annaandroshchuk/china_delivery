'use strict';
/**
 * htmx-config.js
 * Configure HTMX after it loads:
 * - Send Django CSRF token via X-CSRFToken header on every request
 * - This is a belt-and-suspenders approach in addition to the form hidden field
 */
(function () {
    function getCsrfToken() {
        var cookies = document.cookie.split('; ');
        for (var i = 0; i < cookies.length; i++) {
            var parts = cookies[i].split('=');
            if (parts[0] === 'csrftoken') {
                return decodeURIComponent(parts[1]);
            }
        }
        return '';
    }

    document.body.addEventListener('htmx:configRequest', function (e) {
        var token = getCsrfToken();
        if (token) {
            e.detail.headers['X-CSRFToken'] = token;
        }
    });
})();
