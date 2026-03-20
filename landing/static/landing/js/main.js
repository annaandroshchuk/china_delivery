'use strict';

/**
 * main.js
 * - UTM capture + persistence
 * - Header scroll behavior (transparent → frosted)
 * - Burger menu
 * - Benefit card accordion
 * - Smooth scroll
 * - Stat counter animation on scroll
 */

(function () {

    /* ============================================================
       UTM helpers
       ============================================================ */

    var UTM_KEYS = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_content', 'utm_term', 'gclid', 'fbclid'];
    var COOKIE_DAYS = 30;

    function setCookie(name, value, days) {
        var d = new Date();
        d.setTime(d.getTime() + days * 864e5);
        document.cookie = encodeURIComponent(name) + '=' + encodeURIComponent(value) +
            '; expires=' + d.toUTCString() + '; path=/; SameSite=Lax';
    }

    function getCookie(name) {
        var key = encodeURIComponent(name) + '=';
        var parts = document.cookie.split('; ');
        for (var i = 0; i < parts.length; i++) {
            if (parts[i].indexOf(key) === 0) {
                return decodeURIComponent(parts[i].substring(key.length));
            }
        }
        return '';
    }

    function getUrlParams() {
        var params = {};
        var search = window.location.search;
        if (!search) return params;
        search.substring(1).split('&').forEach(function (pair) {
            var kv = pair.split('=');
            if (kv.length === 2) {
                params[decodeURIComponent(kv[0])] = decodeURIComponent(kv[1].replace(/\+/g, ' '));
            }
        });
        return params;
    }

    function captureUtmParams() {
        var urlParams = getUrlParams();
        UTM_KEYS.forEach(function (key) {
            if (urlParams[key]) setCookie(key, urlParams[key], COOKIE_DAYS);
        });
    }

    function getStoredUtm() {
        var stored = {};
        var urlParams = getUrlParams();
        UTM_KEYS.forEach(function (key) {
            stored[key] = urlParams[key] || getCookie(key) || '';
        });
        return stored;
    }

    function injectUtmIntoForm(form) {
        var utm = getStoredUtm();
        UTM_KEYS.forEach(function (key) {
            var input = form.querySelector('input[name="' + key + '"]');
            if (input && utm[key]) input.value = utm[key];
        });
        var pageUrlInput = form.querySelector('.js-page-url');
        if (pageUrlInput) pageUrlInput.value = window.location.href;
    }

    function injectUtmIntoAllForms() {
        document.querySelectorAll('.lead-form').forEach(injectUtmIntoForm);
    }

    /* ============================================================
       Header — transparent over hero, frosted glass on scroll
       ============================================================ */

    function initHeaderScroll() {
        var header = document.getElementById('site-header');
        if (!header) return;

        var scrolled = false;

        function onScroll() {
            var shouldScroll = window.scrollY > 40;
            if (shouldScroll !== scrolled) {
                scrolled = shouldScroll;
                header.classList.toggle('is-scrolled', scrolled);
            }
        }

        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll(); // check initial position
    }

    /* ============================================================
       Burger menu
       ============================================================ */

    function initBurger() {
        var burger   = document.getElementById('header-burger');
        var mobileNav = document.getElementById('header-nav-mobile');
        var backdrop  = document.getElementById('header-mobile-backdrop');
        if (!burger || !mobileNav) return;

        function openMenu() {
            burger.classList.add('is-open');
            burger.setAttribute('aria-expanded', 'true');
            mobileNav.classList.add('is-open');
            mobileNav.setAttribute('aria-hidden', 'false');
            if (backdrop) backdrop.classList.add('is-open');
        }

        function closeMenu() {
            burger.classList.remove('is-open');
            burger.setAttribute('aria-expanded', 'false');
            mobileNav.classList.remove('is-open');
            mobileNav.setAttribute('aria-hidden', 'true');
            if (backdrop) backdrop.classList.remove('is-open');
        }

        burger.addEventListener('click', function () {
            burger.classList.contains('is-open') ? closeMenu() : openMenu();
        });

        if (backdrop) backdrop.addEventListener('click', closeMenu);

        document.addEventListener('keydown', function (e) {
            if (e.key === 'Escape' && burger.classList.contains('is-open')) closeMenu();
        });

        mobileNav.querySelectorAll('a, button').forEach(function (el) {
            el.addEventListener('click', function () { setTimeout(closeMenu, 150); });
        });
    }

    /* ============================================================
       Benefit cards — accordion
       ============================================================ */

    function initBenefitAccordion() {
        document.querySelectorAll('.js-benefit-toggle').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var card  = btn.closest('.benefit-card');
                var body  = card.querySelector('.benefit-body');
                var label = btn.querySelector('.benefit-toggle-label');
                if (!body) return;

                var isOpen = card.classList.contains('is-open');

                if (isOpen) {
                    card.classList.remove('is-open');
                    btn.setAttribute('aria-expanded', 'false');
                    body.setAttribute('data-open', 'false');
                    if (label) label.textContent = 'Детальніше';
                } else {
                    card.classList.add('is-open');
                    btn.setAttribute('aria-expanded', 'true');
                    body.setAttribute('data-open', 'true');
                    if (label) label.textContent = 'Згорнути';
                }
            });
        });
    }

    /* ============================================================
       Stat counters — animated on first scroll into view
       ============================================================ */

    function animateCounter(el, target, duration) {
        var start = 0;
        var startTime = null;
        var suffix = '';

        // Detect suffix (+ or words after digits)
        var raw = el.dataset.target || String(target);
        var match = raw.match(/^(\d+)(.*)$/);
        var num = match ? parseInt(match[1], 10) : target;
        suffix = match ? match[2] : '';

        function step(timestamp) {
            if (!startTime) startTime = timestamp;
            var progress = Math.min((timestamp - startTime) / duration, 1);
            var eased = 1 - Math.pow(1 - progress, 3); // ease-out-cubic
            el.textContent = Math.round(num * eased) + suffix;
            if (progress < 1) requestAnimationFrame(step);
        }

        requestAnimationFrame(step);
    }

    function initStatCounters() {
        var statsEl = document.querySelector('.hero-stats');
        if (!statsEl || !window.IntersectionObserver) return;

        var animated = false;

        var observer = new IntersectionObserver(function (entries) {
            if (animated || !entries[0].isIntersecting) return;
            animated = true;

            statsEl.querySelectorAll('.hero-stat strong').forEach(function (el) {
                var text = el.textContent.trim();
                // e.g. "5000+", "З 2009", "100%", "15+"
                var numMatch = text.match(/\d+/);
                if (!numMatch) return;
                var num = parseInt(numMatch[0], 10);
                var prefix = text.startsWith('З') ? 'З ' : '';
                var suffix = text.includes('+') ? '+' : (text.includes('%') ? '%' : '');
                var duration = num > 1000 ? 1800 : 1200;

                el.textContent = prefix + '0' + suffix;
                var startTime = null;
                (function step(ts) {
                    if (!startTime) startTime = ts;
                    var p = Math.min((ts - startTime) / duration, 1);
                    var eased = 1 - Math.pow(1 - p, 3);
                    el.textContent = prefix + Math.round(num * eased) + suffix;
                    if (p < 1) requestAnimationFrame(step);
                })(performance.now());
            });

            observer.disconnect();
        }, { threshold: 0.5 });

        observer.observe(statsEl);
    }

    /* ============================================================
       Smooth scroll for anchor links
       ============================================================ */

    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function (link) {
            link.addEventListener('click', function (e) {
                var targetId = link.getAttribute('href').slice(1);
                if (!targetId) return;
                var target = document.getElementById(targetId);
                if (!target) return;
                e.preventDefault();
                target.scrollIntoView({ behavior: 'smooth' });
            });
        });
    }

    /* ============================================================
       Init
       ============================================================ */

    function init() {
        captureUtmParams();
        injectUtmIntoAllForms();
        initHeaderScroll();
        initBurger();
        initSmoothScroll();
        initBenefitAccordion();
        initStatCounters();

        // Re-inject UTM after HTMX swaps
        document.body.addEventListener('htmx:afterSwap', function (e) {
            var newForms = e.target.querySelectorAll('.lead-form');
            if (newForms.length === 0 && e.target.classList.contains('lead-form')) {
                injectUtmIntoForm(e.target);
            }
            newForms.forEach(injectUtmIntoForm);
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

})();
