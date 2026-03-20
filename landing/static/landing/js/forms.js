'use strict';

/**
 * forms.js
 * - Popup open/close
 * - HTMX event hooks (form submit, success, error)
 * - dataLayer GTM events on submission
 * - Client-side phone mask (lightweight)
 */

(function () {
    /* ============================================================
       Popup
       ============================================================ */

    var overlay = document.getElementById('popup-overlay');
    var closeBtn = document.getElementById('popup-close');
    var activeFormLocation = 'popup';

    function openPopup(formLocation) {
        if (!overlay) return;
        activeFormLocation = formLocation || 'popup';

        var hiddenFormLocation = overlay.querySelector('input[name="form_location"]');
        if (hiddenFormLocation) {
            hiddenFormLocation.value = activeFormLocation;
        }

        overlay.classList.add('is-open');
        overlay.setAttribute('aria-hidden', 'false');
        document.body.style.overflow = 'hidden';

        // Focus first input in popup
        setTimeout(function () {
            var firstInput = overlay.querySelector('input:not([type="hidden"])');
            if (firstInput) firstInput.focus();
        }, 100);
    }

    function closePopup() {
        if (!overlay) return;
        overlay.classList.remove('is-open');
        overlay.setAttribute('aria-hidden', 'true');
        document.body.style.overflow = '';
    }

    function initPopup() {
        if (!overlay) return;

        document.querySelectorAll('.js-open-popup').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var loc = btn.dataset.formLocation || 'popup';
                openPopup(loc);
            });
        });

        if (closeBtn) {
            closeBtn.addEventListener('click', closePopup);
        }

        overlay.addEventListener('click', function (e) {
            if (e.target === overlay) closePopup();
        });

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && overlay.classList.contains('is-open')) {
                closePopup();
            }
        });
    }

    /* ============================================================
       Phone input — allow natural input, light cleanup on blur
       ============================================================ */

    function initPhoneMasks() {
        document.querySelectorAll('input[type="tel"]').forEach(function (input) {
            // Allow typing freely, only strip truly invalid chars on blur
            input.addEventListener('blur', function () {
                var raw = input.value.trim();
                if (!raw) return;
                // Remove everything except digits, +, -, (, ), space
                raw = raw.replace(/[^\d+\-() ]/g, '');
                // If starts with 0, prepend +38
                if (/^0\d/.test(raw)) {
                    raw = '+38' + raw;
                }
                // If starts with 380, prepend +
                if (/^380\d/.test(raw)) {
                    raw = '+' + raw;
                }
                input.value = raw;
            });
        });
    }

    /* ============================================================
       GTM dataLayer push on form submit
       ============================================================ */

    function pushGtmEvent(eventName, formLocation) {
        if (typeof window.dataLayer !== 'undefined') {
            window.dataLayer.push({
                event: eventName,
                form_location: formLocation,
            });
        }
    }

    /* ============================================================
       HTMX hooks
       ============================================================ */

    function initHtmxHooks() {
        document.body.addEventListener('htmx:beforeRequest', function (e) {
            var form = e.target.closest('.lead-form');
            if (!form) return;
            var loc = form.dataset.formLocation || 'unknown';
            pushGtmEvent('form_submit_attempt', loc);
        });

        document.body.addEventListener('htmx:afterSwap', function (e) {
            var successMsg = e.target.querySelector('.success-message');
            if (successMsg) {
                var form = e.target.closest('[id^="form-wrapper-"]');
                var loc = form ? form.id.replace('form-wrapper-', '') : 'unknown';
                pushGtmEvent('form_submit_success', loc);

                // If success in popup, close after a short delay
                if (loc === 'popup' && overlay && overlay.classList.contains('is-open')) {
                    setTimeout(closePopup, 4000);
                }
            }
        });

        document.body.addEventListener('htmx:responseError', function (e) {
            var form = e.target.closest('.lead-form');
            if (!form) return;
            pushGtmEvent('form_submit_error', form.dataset.formLocation || 'unknown');
        });
    }

    /* ============================================================
       Init
       ============================================================ */

    function init() {
        initPopup();
        initPhoneMasks();
        initHtmxHooks();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
