'use strict';

/**
 * faq.js
 * Smooth CSS-grid accordion for:
 *   - FAQ section
 *   - Problems/Solutions expandables
 *   - Cooperation cards
 *   - Benefit cards (handled in main.js)
 *   - What-we-dont toggle
 */

(function () {

    /* ---- Generic smooth accordion helper ---- */

    function setupSmoothAccordion(containerSelector, itemSelector, buttonSelector, bodySelector) {
        var container = document.querySelector(containerSelector);
        if (!container) return;

        container.querySelectorAll(buttonSelector).forEach(function (btn) {
            btn.addEventListener('click', function () {
                var item = btn.closest(itemSelector);
                if (!item) return;
                var body = item.querySelector(bodySelector);
                if (!body) return;

                var isExpanded = btn.getAttribute('aria-expanded') === 'true';
                btn.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
                body.setAttribute('data-open', isExpanded ? 'false' : 'true');
            });
        });
    }

    /* ---- FAQ ---- */

    function initFaq() {
        var list = document.querySelector('.faq-list');
        if (!list) return;

        list.querySelectorAll('.faq-question').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var item = btn.closest('.faq-item');
                var body = item.querySelector('.faq-answer');
                if (!body) return;

                var isExpanded = btn.getAttribute('aria-expanded') === 'true';
                btn.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
                body.setAttribute('data-open', isExpanded ? 'false' : 'true');
            });
        });
    }

    /* ---- Problems → Solutions expandables ---- */

    function initSolutionExpanders() {
        document.querySelectorAll('.js-expandable').forEach(function (item) {
            var btn = item.querySelector('.ps-solution-header');
            var body = item.querySelector('.ps-solution-body');
            if (!btn || !body) return;

            btn.addEventListener('click', function () {
                var isExpanded = btn.getAttribute('aria-expanded') === 'true';
                btn.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
                body.setAttribute('data-open', isExpanded ? 'false' : 'true');
            });
        });
    }

    /* ---- Cooperation cards ---- */

    function initCoopCards() {
        document.querySelectorAll('.js-expandable-card').forEach(function (card) {
            var btn = card.querySelector('.coop-card-toggle');
            var details = card.querySelector('.coop-card-details');
            if (!btn || !details) return;

            btn.addEventListener('click', function () {
                var isExpanded = btn.getAttribute('aria-expanded') === 'true';
                btn.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
                details.setAttribute('data-open', isExpanded ? 'false' : 'true');
            });
        });
    }

    /* ---- What we don't deliver toggle ---- */

    function initDontToggle() {
        var btn = document.getElementById('dont-toggle');
        var body = document.getElementById('dont-body');
        if (!btn || !body) return;

        btn.addEventListener('click', function () {
            var isExpanded = btn.getAttribute('aria-expanded') === 'true';
            btn.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
            body.setAttribute('data-open', isExpanded ? 'false' : 'true');
        });
    }

    /* ---- Init ---- */

    function init() {
        initFaq();
        initSolutionExpanders();
        initCoopCards();
        initDontToggle();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
