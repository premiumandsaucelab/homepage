// Clean, minimalistic design requires minimal JS.
// We can add subtle entrance animations here if needed.

document.addEventListener('DOMContentLoaded', () => {
    const nodes = document.querySelectorAll('.org-node');
    
    // Simple staggered fade-in animation
    nodes.forEach((node, index) => {
        node.style.opacity = '0';
        node.style.transform = 'translateY(20px)';
        node.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        
        setTimeout(() => {
            node.style.opacity = '1';
            node.style.transform = 'translateY(0)';
        }, 100 * index);
    });

    // Scroll Reveal Animation
    const revealElements = document.querySelectorAll('.reveal, .reveal-left');
    const revealOptions = {
        threshold: 0.1,
        rootMargin: "0px 0px -50px 0px"
    };

    const revealOnScroll = new IntersectionObserver(function(entries, observer) {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            entry.target.classList.add('active');
            observer.unobserve(entry.target);
        });
    }, revealOptions);

    revealElements.forEach(el => {
        revealOnScroll.observe(el);
    });

    // --- Number Count-up Animation ---
    const countElements = document.querySelectorAll('.count-up');
    const countObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (!entry.isIntersecting) return;
            const target = entry.target;
            const endVal = parseFloat(target.getAttribute('data-target'));
            const duration = 2000;
            let startTimestamp = null;
            
            const step = (timestamp) => {
                if (!startTimestamp) startTimestamp = timestamp;
                const progress = Math.min((timestamp - startTimestamp) / duration, 1);
                // easeOutQuart
                const easeProgress = 1 - Math.pow(1 - progress, 4);
                
                const currentVal = (easeProgress * endVal).toFixed(endVal % 1 !== 0 ? 1 : 0);
                target.innerText = currentVal;
                
                if (progress < 1) {
                    window.requestAnimationFrame(step);
                } else {
                    target.innerText = endVal;
                }
            };
            window.requestAnimationFrame(step);
            observer.unobserve(target);
        });
    }, { threshold: 0.1 });

    countElements.forEach(el => {
        countObserver.observe(el);
    });

    // --- Mobile Hamburger Menu Injection & Toggle ---
    const navContainer = document.querySelector('.nav-container');
    const navLinks = document.querySelector('.nav-links');
    
    if (navContainer && navLinks && !document.querySelector('.hamburger')) {
        // Create hamburger button dynamically
        const hamburger = document.createElement('button');
        hamburger.className = 'hamburger';
        hamburger.setAttribute('aria-label', '메뉴 열기');
        hamburger.innerHTML = '<span></span><span></span><span></span>';
        navContainer.appendChild(hamburger);
        
        // Toggle logic
        hamburger.addEventListener('click', () => {
            hamburger.classList.toggle('open');
            navLinks.classList.toggle('active');
            document.body.style.overflow = navLinks.classList.contains('active') ? 'hidden' : '';
        });

        // Close menu when a link is clicked
        const links = navLinks.querySelectorAll('a');
        links.forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('open');
                navLinks.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // Highlighter Micro-animation Observer
    const highlightElements = document.querySelectorAll('.highlight-anim');
    const highlightObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.5,
        rootMargin: "0px 0px -50px 0px"
    });

    highlightElements.forEach(el => highlightObserver.observe(el));
});
