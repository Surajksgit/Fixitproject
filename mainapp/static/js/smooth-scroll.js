/**
 * FIXIT - Universal Smooth Scrolling Engine (Lenis)
 * Provides silky, inertial mouse wheel & touchpad smooth scrolling across all pages.
 */
(function () {
    'use strict';

    if (typeof Lenis === 'undefined') {
        return;
    }

    // Initialize Lenis with refined easing and inertia settings
    const lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
        wheelMultiplier: 1.0,
        touchMultiplier: 1.5,
        infinite: false,
    });

    window.lenis = lenis;

    function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // Sync with GSAP ScrollTrigger if present
    if (typeof ScrollTrigger !== 'undefined' && typeof gsap !== 'undefined') {
        lenis.on('scroll', ScrollTrigger.update);
        gsap.ticker.add((time) => {
            lenis.raf(time * 1000);
        });
        gsap.ticker.lagSmoothing(0);
    }

    // Smooth Anchor Navigation
    document.addEventListener('DOMContentLoaded', function () {
        document.querySelectorAll('a[href^="#"]').forEach(function (anchor) {
            anchor.addEventListener('click', function (e) {
                const targetId = this.getAttribute('href');
                if (targetId && targetId.length > 1 && targetId.startsWith('#')) {
                    const targetEl = document.querySelector(targetId);
                    if (targetEl) {
                        e.preventDefault();
                        lenis.scrollTo(targetEl, { offset: -20, duration: 1.2 });
                    }
                }
            });
        });
    });

    // Pause Lenis during Bootstrap modal display to allow modal internal scrolling
    document.addEventListener('show.bs.modal', function () {
        if (window.lenis) window.lenis.stop();
    });

    document.addEventListener('hidden.bs.modal', function () {
        if (window.lenis) window.lenis.start();
    });
})();
