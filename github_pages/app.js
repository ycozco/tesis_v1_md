
document.addEventListener('DOMContentLoaded', () => {
    // Theme toggler
    const toggleSwitch = document.querySelector('.theme-switch input[type="checkbox"]');
    const currentTheme = localStorage.getItem('theme') ? localStorage.getItem('theme') : null;

    if (currentTheme) {
        document.documentElement.setAttribute('data-theme', currentTheme);
        if (currentTheme === 'dark') {
            toggleSwitch.checked = true;
        }
    }

    toggleSwitch.addEventListener('change', function(e) {
        if (e.target.checked) {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-theme', 'light');
            localStorage.setItem('theme', 'light');
        }    
    });

    // Back to top button
    const backToTopBtn = document.getElementById('back-to-top');
    window.addEventListener('scroll', () => {
        if (window.scrollY > 300) {
            backToTopBtn.style.display = 'block';
        } else {
            backToTopBtn.style.display = 'none';
        }
    });

    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Highlight active section in TOC
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                if (id) {
                    document.querySelectorAll('.toc-container a').forEach(a => {
                        a.style.fontWeight = 'normal';
                        a.style.color = 'var(--text-color)';
                        if (a.getAttribute('href') === '#' + id) {
                            a.style.fontWeight = 'bold';
                            a.style.color = 'var(--primary-color)';
                        }
                    });
                }
            }
        });
    }, { rootMargin: '-20% 0px -80% 0px' });

    document.querySelectorAll('.paper h1, .paper h2, .paper h3').forEach(h => observer.observe(h));
});
