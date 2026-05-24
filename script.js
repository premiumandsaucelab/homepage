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
});
