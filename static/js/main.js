// Mobile Menu Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger) {
        hamburger.addEventListener('click', function() {
            navMenu.classList.toggle('active');
            
            // Animate hamburger
            const spans = hamburger.querySelectorAll('span');
            spans[0].style.transform = navMenu.classList.contains('active') 
                ? 'rotate(-45deg) translate(-5px, 6px)' 
                : 'none';
            spans[1].style.opacity = navMenu.classList.contains('active') ? '0' : '1';
            spans[2].style.transform = navMenu.classList.contains('active') 
                ? 'rotate(45deg) translate(-5px, -6px)' 
                : 'none';
        });
        
        // Close menu when clicking on a link
        const navLinks = document.querySelectorAll('.nav-link, .btn');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                navMenu.classList.remove('active');
                const spans = hamburger.querySelectorAll('span');
                spans[0].style.transform = 'none';
                spans[1].style.opacity = '1';
                spans[2].style.transform = 'none';
            });
        });
    }
});

// Flash Messages Auto-Hide
document.addEventListener('DOMContentLoaded', function() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Add click event to close button
        const closeBtn = alert.querySelector('.close-alert');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
        }
        
        // Auto-hide after 5 seconds
        setTimeout(() => {
            if (alert.parentElement) {
                alert.style.animation = 'slideOutRight 0.3s ease';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            }
        }, 5000);
    });
});

// Add slideOutRight animation
const style = document.createElement('style');
style.textContent = `
    @keyframes slideOutRight {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(400px);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// Smooth Scroll for Anchor Links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Scroll to Top Button
const scrollToTopBtn = document.createElement('button');
scrollToTopBtn.innerHTML = '↑';
scrollToTopBtn.className = 'scroll-to-top';
scrollToTopBtn.style.cssText = `
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 50px;
    height: 50px;
    background: linear-gradient(135deg, #1e5a7d, #2d8659);
    color: white;
    border: none;
    border-radius: 50%;
    font-size: 1.5rem;
    cursor: pointer;
    opacity: 0;
    visibility: hidden;
    transition: all 0.3s ease;
    z-index: 1000;
    box-shadow: 0 4px 15px rgba(0,0,0,0.2);
`;

document.body.appendChild(scrollToTopBtn);

window.addEventListener('scroll', () => {
    if (window.pageYOffset > 300) {
        scrollToTopBtn.style.opacity = '1';
        scrollToTopBtn.style.visibility = 'visible';
    } else {
        scrollToTopBtn.style.opacity = '0';
        scrollToTopBtn.style.visibility = 'hidden';
    }
});

scrollToTopBtn.addEventListener('click', () => {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

scrollToTopBtn.addEventListener('mouseenter', () => {
    scrollToTopBtn.style.transform = 'scale(1.1)';
});

scrollToTopBtn.addEventListener('mouseleave', () => {
    scrollToTopBtn.style.transform = 'scale(1)';
});

// Form Validation Enhancement
document.querySelectorAll('form').forEach(form => {
    form.addEventListener('submit', function(e) {
        const inputs = this.querySelectorAll('input[required], textarea[required]');
        let isValid = true;
        
        inputs.forEach(input => {
            if (!input.value.trim()) {
                isValid = false;
                input.style.borderColor = '#dc3545';
            } else {
                input.style.borderColor = '#28a745';
            }
        });
        
        if (!isValid) {
            e.preventDefault();
            // Show error message
            const existingError = this.querySelector('.form-error');
            if (!existingError) {
                const errorDiv = document.createElement('div');
                errorDiv.className = 'form-error alert alert-danger';
                errorDiv.textContent = 'Please fill in all required fields.';
                errorDiv.style.marginBottom = '1rem';
                this.insertBefore(errorDiv, this.firstChild);
                
                setTimeout(() => {
                    errorDiv.remove();
                }, 3000);
            }
        }
    });
});

// Add animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.animation = 'fadeInUp 0.6s ease forwards';
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe cards and sections
document.addEventListener('DOMContentLoaded', () => {
    const animatedElements = document.querySelectorAll(
        '.feature-card, .course-card, .stat-card, .enrollment-card, .course-card-detailed'
    );
    
    animatedElements.forEach(el => {
        el.style.opacity = '0';
        observer.observe(el);
    });
});

// Number Counter Animation for Stats
function animateCounter(element, target, duration = 2000) {
    let start = 0;
    const increment = target / (duration / 16);
    const timer = setInterval(() => {
        start += increment;
        if (start >= target) {
            element.textContent = target + (element.dataset.suffix || '');
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(start) + (element.dataset.suffix || '');
        }
    }, 16);
}

// Animate counters when they come into view
const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
            entry.target.classList.add('counted');
            const text = entry.target.textContent;
            const number = parseInt(text.replace(/\D/g, ''));
            const suffix = text.replace(/[0-9]/g, '');
            entry.target.dataset.suffix = suffix;
            animateCounter(entry.target, number);
        }
    });
}, { threshold: 0.5 });

document.addEventListener('DOMContentLoaded', () => {
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => counterObserver.observe(stat));
});

// Payment Method Selection Visual Feedback
document.querySelectorAll('.payment-option').forEach(option => {
    option.addEventListener('click', function() {
        document.querySelectorAll('.payment-option').forEach(opt => {
            opt.style.transform = 'scale(1)';
        });
        this.style.transform = 'scale(1.02)';
    });
});

// Console welcome message
console.log('%c💧 Welcome to Raindrops Academy! 📖', 'color: #1e5a7d; font-size: 20px; font-weight: bold;');
console.log('%cMay Allah bless your learning journey.', 'color: #2d8659; font-size: 14px;');
