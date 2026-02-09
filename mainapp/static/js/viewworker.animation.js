document.addEventListener('DOMContentLoaded', function () {
    // Register GSAP Plugins
    gsap.registerPlugin(ScrollTrigger);

    // Initialize Lenis Smooth Scroll
    const lenis = new Lenis({
        duration: 1.2,
        easing: (t) => Math.min(1, 1.001 - Math.pow(2, -10 * t)),
        orientation: 'vertical',
        gestureOrientation: 'vertical',
        smoothWheel: true,
        wheelMultiplier: 1,
        smoothTouch: false,
        touchMultiplier: 2,
        infinite: false,
    });

    function raf(time) {
        lenis.raf(time);
        requestAnimationFrame(raf);
    }
    requestAnimationFrame(raf);

    // Custom Cursor Logic
    const cursorDot = document.querySelector('.cursor-dot');
    const cursorOutline = document.querySelector('.cursor-outline');

    window.addEventListener('mousemove', (e) => {
        const posX = e.clientX;
        const posY = e.clientY;

        gsap.to(cursorDot, {
            x: posX,
            y: posY,
            duration: 0.1,
            ease: "power2.out"
        });

        gsap.to(cursorOutline, {
            x: posX,
            y: posY,
            duration: 0.5,
            ease: "power3.out"
        });
    });

    // Cursor Hover Effects
    const interactiveElements = document.querySelectorAll('a, button, .info-card-premium, .tag');
    interactiveElements.forEach(el => {
        el.addEventListener('mouseenter', () => {
            gsap.to(cursorOutline, {
                scale: 1.5,
                backgroundColor: 'rgba(99, 102, 241, 0.1)',
                borderWidth: '1px',
                duration: 0.3
            });
        });
        el.addEventListener('mouseleave', () => {
            gsap.to(cursorOutline, {
                scale: 1,
                backgroundColor: 'transparent',
                borderWidth: '2px',
                duration: 0.3
            });
        });
    });

    // Split Type Animations
    const splitTexts = document.querySelectorAll('.split-text');
    splitTexts.forEach(text => {
        new SplitType(text, { types: 'words,chars' });
    });

    const revealTexts = document.querySelectorAll('.reveal-text');
    revealTexts.forEach(text => {
        const split = new SplitType(text, { types: 'chars' });
        gsap.from(split.chars, {
            scrollTrigger: {
                trigger: text,
                start: "top 90%",
                toggleActions: "play none none reverse"
            },
            y: 100,
            opacity: 0,
            rotateX: -90,
            stagger: 0.02,
            duration: 1.2,
            ease: "power4.out"
        });
    });

    // Hero Animation Timeline
    const heroTl = gsap.timeline({ defaults: { ease: "power4.out" } });

    heroTl.from('.navbar', {
        y: -100,
        opacity: 0,
        duration: 1
    })
        .from('.premium-badge', {
            scale: 0.8,
            opacity: 0,
            duration: 0.8
        }, "-=0.5")
        .from('.hero-name .reveal-text', {
            y: 100,
            stagger: 0.1,
            duration: 1.2
        }, "-=0.8")
        .from('.hero-lead .word', {
            y: 20,
            opacity: 0,
            stagger: 0.02,
            duration: 1
        }, "-=1")
        .from('.stat-box', {
            y: 30,
            opacity: 0,
            stagger: 0.1,
            duration: 0.8
        }, "-=0.8")
        .from('.hero-actions', {
            y: 30,
            opacity: 0,
            duration: 0.8
        }, "-=0.6")
        .from('.image-inner', {
            scale: 0.8,
            opacity: 0,
            rotateY: 20,
            duration: 1.5
        }, "0.5")
        .from('.floating-info-card', {
            x: 50,
            opacity: 0,
            stagger: 0.2,
            duration: 1
        }, "-=1")
        .from('.availability-status', {
            y: -20,
            opacity: 0,
            duration: 0.8
        }, "-=0.8");

    // Parallax Effect for Floating Cards
    document.addEventListener('mousemove', (e) => {
        const moveX = (e.clientX - window.innerWidth / 2) * 0.02;
        const moveY = (e.clientY - window.innerHeight / 2) * 0.02;

        gsap.to('.floating-info-card', {
            x: (i, target) => moveX * parseFloat(target.dataset.parallax || 1) * 20,
            y: (i, target) => moveY * parseFloat(target.dataset.parallax || 1) * 20,
            duration: 1,
            ease: "power2.out"
        });
    });

    // Stat Counter Animation
    const stats = document.querySelectorAll('.stat-val');
    stats.forEach(stat => {
        const target = parseFloat(stat.dataset.target);
        gsap.from(stat, {
            scrollTrigger: {
                trigger: stat,
                start: "top 95%",
            },
            innerText: 0,
            duration: 2,
            snap: { innerText: target % 1 === 0 ? 1 : 0.1 },
            ease: "power2.out"
        });
    });

    // Section Scroll Animations
    gsap.from('.info-card-premium', {
        scrollTrigger: {
            trigger: '.details-section',
            start: "top 70%",
        },
        y: 50,
        opacity: 0,
        stagger: 0.1,
        duration: 1,
        ease: "power3.out"
    });

    gsap.from('.glass-container', {
        scrollTrigger: {
            trigger: '.worker-description',
            start: "top 80%",
        },
        y: 40,
        opacity: 0,
        duration: 1.2,
        ease: "power3.out"
    });

    // Navbar Scrolled State
    ScrollTrigger.create({
        start: "top -50",
        onEnter: () => document.querySelector('.custom-nav').classList.add('scrolled'),
        onLeaveBack: () => document.querySelector('.custom-nav').classList.remove('scrolled'),
    });

    // CTA Animation
    gsap.from('.cta-card', {
        scrollTrigger: {
            trigger: '.cta-section',
            start: "top 80%",
        },
        scale: 0.9,
        opacity: 0,
        duration: 1.5,
        ease: "power4.out"
    });
});
