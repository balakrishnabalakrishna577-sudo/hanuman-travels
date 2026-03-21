// ===== Hanuman Tours - Main JavaScript =====

document.addEventListener('DOMContentLoaded', function () {

    // Navbar scroll effect
    const navbar = document.querySelector('.navbar');
    window.addEventListener('scroll', function () {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    });

    // Back to top button
    const backToTop = document.getElementById('backToTop');
    if (backToTop) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 400) {
                backToTop.classList.add('show');
            } else {
                backToTop.classList.remove('show');
            }
        });
        backToTop.addEventListener('click', function () {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // Wishlist toggle
    document.querySelectorAll('.wishlist-btn').forEach(function (btn) {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            e.stopPropagation();
            const tourId = btn.dataset.tourId;
            // Get CSRF token from the global hidden form or cookie
            const csrfInput = document.querySelector('#csrf-form [name=csrfmiddlewaretoken]');
            const csrfToken = csrfInput ? csrfInput.value : getCookie('csrftoken');
            fetch('/wishlist/toggle/' + tourId + '/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': csrfToken,
                    'Content-Type': 'application/json',
                },
                credentials: 'same-origin',
            })
            .then(function(r) {
                if (r.status === 401) return r.json().then(function(d) { return d; });
                return r.json();
            })
            .then(function(data) {
                if (data.status === 'added') {
                    btn.classList.add('active');
                    btn.querySelector('i').className = 'bi bi-heart-fill';
                    btn.title = 'Remove from wishlist';
                } else if (data.status === 'removed') {
                    btn.classList.remove('active');
                    btn.querySelector('i').className = 'bi bi-heart';
                    btn.title = 'Add to wishlist';
                } else if (data.status === 'login_required') {
                    window.location.href = '/users/login/?next=' + encodeURIComponent(window.location.pathname);
                }
            })
            .catch(function() {});
        });
    });

    // Auto-dismiss alerts after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Booking price calculator
    const numAdults = document.getElementById('id_num_adults');
    const numChildren = document.getElementById('id_num_children');
    const priceDisplay = document.getElementById('total-price');

    if (numAdults && priceDisplay) {
        const pricePerPerson = parseFloat(priceDisplay.dataset.price || 0);

        function updatePrice() {
            const adults = parseInt(numAdults.value) || 0;
            const children = numChildren ? parseInt(numChildren.value) || 0 : 0;
            const total = pricePerPerson * (adults + children);
            priceDisplay.textContent = '₹' + total.toLocaleString('en-IN');
        }

        numAdults.addEventListener('input', updatePrice);
        if (numChildren) numChildren.addEventListener('input', updatePrice);
    }

    // Car rental price calculator
    const pickupDate = document.getElementById('id_pickup_date');
    const returnDate = document.getElementById('id_return_date');
    const carPriceDisplay = document.getElementById('car-total-price');

    if (pickupDate && returnDate && carPriceDisplay) {
        const pricePerDay = parseFloat(carPriceDisplay.dataset.price || 0);

        function updateCarPrice() {
            const pickup = new Date(pickupDate.value);
            const ret = new Date(returnDate.value);
            if (pickup && ret && ret > pickup) {
                const days = Math.ceil((ret - pickup) / (1000 * 60 * 60 * 24));
                const total = pricePerDay * days;
                carPriceDisplay.textContent = '₹' + total.toLocaleString('en-IN') + ' (' + days + ' days)';
            }
        }

        pickupDate.addEventListener('change', updateCarPrice);
        returnDate.addEventListener('change', updateCarPrice);
    }

    // Set minimum date for date inputs to today
    const dateInputs = document.querySelectorAll('input[type="date"]');
    const today = new Date().toISOString().split('T')[0];
    dateInputs.forEach(function (input) {
        if (!input.min) {
            input.min = today;
        }
    });

    // Gallery lightbox effect (simple)
    const galleryItems = document.querySelectorAll('.gallery-item');
    galleryItems.forEach(function (item) {
        item.addEventListener('click', function () {
            const img = item.querySelector('img');
            if (img) {
                const modal = document.createElement('div');
                modal.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(0,0,0,0.9);z-index:99999;display:flex;align-items:center;justify-content:center;cursor:pointer;';
                const imgEl = document.createElement('img');
                imgEl.src = img.src;
                imgEl.style.cssText = 'max-width:90%;max-height:90vh;border-radius:8px;';
                modal.appendChild(imgEl);
                modal.addEventListener('click', function () { document.body.removeChild(modal); });
                document.body.appendChild(modal);
            }
        });
    });

    // Smooth counter animation for stats
    const counters = document.querySelectorAll('.stat-box h2, .stat-box h3, .stat-box h4');
    const observerOptions = { threshold: 0.5 };

    const observer = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
            if (entry.isIntersecting) {
                const el = entry.target;
                const target = parseInt(el.textContent.replace(/\D/g, ''));
                const suffix = el.textContent.replace(/[0-9]/g, '');
                let current = 0;
                const increment = target / 50;
                const timer = setInterval(function () {
                    current += increment;
                    if (current >= target) {
                        current = target;
                        clearInterval(timer);
                    }
                    el.textContent = Math.floor(current) + suffix;
                }, 30);
                observer.unobserve(el);
            }
        });
    }, observerOptions);

    counters.forEach(function (counter) { observer.observe(counter); });

    // Tour type filter active state
    const filterBtns = document.querySelectorAll('[data-filter]');
    filterBtns.forEach(function (btn) {
        btn.addEventListener('click', function () {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
        });
    });

    // Social share copy link
    document.querySelectorAll('.share-copy-btn').forEach(function (btn) {
        btn.addEventListener('click', function () {
            navigator.clipboard.writeText(window.location.href).then(function () {
                const orig = btn.innerHTML;
                btn.innerHTML = '<i class="bi bi-check2 me-1"></i>Copied!';
                setTimeout(function () { btn.innerHTML = orig; }, 2000);
            });
        });
    });
});

// CSRF cookie helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(function (cookie) {
            const c = cookie.trim();
            if (c.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(c.slice(name.length + 1));
            }
        });
    }
    return cookieValue;
}
