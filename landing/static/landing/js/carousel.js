'use strict';

/**
 * carousel.js
 * Initializes Swiper for the product categories carousel.
 */

(function () {
    function initCategoriesSwiper() {
        var el = document.getElementById('categories-swiper');
        if (!el || typeof Swiper === 'undefined') return;

        new Swiper(el, {
            slidesPerView: 1.3,
            spaceBetween: 16,
            loop: false,
            grabCursor: true,
            pagination: {
                el: el.querySelector('.categories-pagination'),
                clickable: true,
                dynamicBullets: true,
            },
            navigation: {
                prevEl: el.querySelector('.categories-prev'),
                nextEl: el.querySelector('.categories-next'),
            },
            a11y: {
                prevSlideMessage: 'Попередній слайд',
                nextSlideMessage: 'Наступний слайд',
            },
            breakpoints: {
                480: {
                    slidesPerView: 2,
                    spaceBetween: 14,
                },
                640: {
                    slidesPerView: 2.5,
                    spaceBetween: 16,
                },
                768: {
                    slidesPerView: 3,
                    spaceBetween: 20,
                },
                992: {
                    slidesPerView: 4,
                    spaceBetween: 24,
                },
                1200: {
                    slidesPerView: 5,
                    spaceBetween: 24,
                },
            },
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initCategoriesSwiper);
    } else {
        initCategoriesSwiper();
    }
})();
