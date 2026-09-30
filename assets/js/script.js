/* ============================================================
   Worksheet Wonder — script.js
   Shared behavior for content & account pages (no database).
   Includes: nav state, back-to-top, footer year, AOS guard,
   newsletter, contact form, demo auth, demo cart & checkout.
   ============================================================ */
(function () {
    'use strict';

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    function store(key, val) {
        try {
            if (val === undefined) return JSON.parse(localStorage.getItem(key) || 'null');
            localStorage.setItem(key, JSON.stringify(val));
        } catch (e) { return null; }
    }

    function toast(msg) {
        var t = document.createElement('div');
        t.className = 'alert alert-success position-fixed top-0 start-50 translate-middle-x mt-3 shadow';
        t.style.zIndex = '2000';
        t.textContent = msg;
        document.body.appendChild(t);
        setTimeout(function () { t.remove(); }, 2600);
    }

    /* ---------- Chrome ---------- */
    function initChrome() {
        var page = (location.pathname.split('/').pop() || 'index.html').split('?')[0].toLowerCase();
        document.querySelectorAll('.navbar-nav .nav-link').forEach(function (a) {
            var href = (a.getAttribute('href') || '').toLowerCase();
            if (href && href === page) a.classList.add('active');
        });

        var btn = document.getElementById('backToTop');
        if (!btn) {
            btn = document.createElement('button');
            btn.id = 'backToTop';
            btn.setAttribute('aria-label', 'Back to top');
            btn.innerHTML = '↑';
            document.body.appendChild(btn);
        }
        window.addEventListener('scroll', function () {
            btn.classList.toggle('show', window.scrollY > 400);
        }, { passive: true });
        btn.addEventListener('click', function () { window.scrollTo({ top: 0, behavior: 'smooth' }); });

        document.querySelectorAll('[data-year]').forEach(function (el) {
            el.textContent = new Date().getFullYear();
        });

        if (typeof AOS !== 'undefined' && AOS && AOS.init && !window.__aosInit) {
            try { AOS.init({ duration: 900, once: true }); window.__aosInit = true; } catch (e) {}
        }

        document.querySelectorAll('.newsletter-form').forEach(function (form) {
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                var input = form.querySelector('input[type="email"]');
                if (input && input.value) {
                    form.innerHTML = '<div class="alert alert-success mb-0">🎉 You are subscribed! Check your inbox for a welcome gift.</div>';
                }
            });
        });
    }

    /* ---------- Contact form ---------- */
    function initContact() {
        var form = document.getElementById('contact-form');
        if (!form) return;
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            form.innerHTML = '<div class="alert alert-success">✅ Thank you! Your message has been sent. We reply within 1–2 business days.</div>';
        });
    }

    /* ---------- Demo auth ---------- */
    function initAuth() {
        var login = document.getElementById('login-form');
        if (login) login.addEventListener('submit', function (e) {
            e.preventDefault();
            var email = document.getElementById('email');
            store('ww_user', { name: (email && email.value.split('@')[0]) || 'Friend', email: email && email.value, plan: 'Free' });
            toast('👋 Welcome back!');
            setTimeout(function () { location.href = 'portal.html'; }, 900);
        });
        var reg = document.getElementById('register-form');
        if (reg) reg.addEventListener('submit', function (e) {
            e.preventDefault();
            var fn = document.getElementById('firstName'), em = document.getElementById('email');
            store('ww_user', { name: (fn && fn.value) || 'Friend', email: em && em.value, plan: 'Free' });
            toast('🎉 Account created!');
            setTimeout(function () { location.href = 'portal.html'; }, 900);
        });
    }

    /* ---------- Demo cart & checkout ---------- */
    function cart() { return store('ww_cart') || []; }
    function saveCart(c) { store('ww_cart', c); renderCartCount(); }
    function renderCartCount() {
        document.querySelectorAll('[data-cart-count]').forEach(function (el) {
            el.textContent = cart().length;
        });
    }
    /* ---------- Cart page table (cart.html) ---------- */
    function money(n) { return '$' + n.toFixed(2); }
    function renderCartTable() {
        var tbody = document.getElementById('cart-tbody');
        if (!tbody) return;
        var items = cart();
        if (!items.length) {
            tbody.innerHTML = '<tr><td colspan="4" class="p-5 text-center">' +
                '<div class="empty-state"><span class="empty-icon">🛒</span><h5>Your cart is empty</h5>' +
                '<p><a href="shop.html" class="btn btn-rainbow btn-sm mt-2">Browse bundles</a></p></div></td></tr>';
        } else {
            tbody.innerHTML = items.map(function (it, i) {
                return '<tr class="border-bottom">' +
                    '<td class="p-4"><div class="d-flex align-items-center"><div class="ms-3">' +
                    '<h6 class="fw-bold mb-1">' + it.title + '</h6>' +
                    '<small class="text-muted">' + it.meta + '</small></div></div></td>' +
                    '<td>' + money(it.price) + '</td>' +
                    '<td class="text-center"><span class="fw-bold">1</span><br>' +
                    '<a href="#" class="text-danger small text-decoration-none mt-1 d-inline-block" data-remove="' + i + '">' +
                    '<i class="bi bi-trash"></i> Remove</a></td>' +
                    '<td class="text-end fw-bold px-4 text-primary">' + money(it.price) + '</td></tr>';
            }).join('');
        }
        var sub = items.reduce(function (s, it) { return s + it.price; }, 0);
        var tax = sub * 0.18;
        setText('cart-subtotal', money(sub));
        setText('cart-tax', money(tax));
        setText('cart-total', money(sub + tax));
        tbody.querySelectorAll('[data-remove]').forEach(function (a) {
            a.addEventListener('click', function (e) {
                e.preventDefault();
                var c = cart(); c.splice(+a.getAttribute('data-remove'), 1); saveCart(c); renderCartTable();
            });
        });
        var clear = document.getElementById('cart-clear');
        if (clear && !clear.__wwBound) {
            clear.__wwBound = true;
            clear.addEventListener('click', function () { saveCart([]); renderCartTable(); });
        }
    }
    function setText(id, text) {
        var el = document.getElementById(id);
        if (el) el.textContent = text;
    }

    function initCart() {
        renderCartCount();
        var grid = document.getElementById('cart-items');
        if (grid) {
            var items = cart();
            grid.innerHTML = items.length ? items.map(function (it, i) {
                return '<div class="d-flex justify-content-between align-items-center border-bottom py-3">' +
                    '<div><strong>' + it.title + '</strong><br><small class="text-muted">' + it.meta + '</small></div>' +
                    '<div class="d-flex align-items-center gap-3"><span class="price">' + money(it.price) + '</span>' +
                    '<button class="btn btn-outline-danger btn-sm" data-remove="' + i + '">Remove</button></div></div>';
            }).join('') : '<div class="empty-state"><span class="empty-icon">🛒</span><h5>Your cart is empty</h5><p><a href="shop.html" class="btn btn-rainbow btn-sm mt-2">Browse bundles</a></p></div>';
            var total = items.reduce(function (s, it) { return s + it.price; }, 0);
            var totalEl = document.getElementById('cart-total');
            if (totalEl) totalEl.textContent = money(total);
            grid.querySelectorAll('[data-remove]').forEach(function (b) {
                b.addEventListener('click', function () {
                    var c = cart(); c.splice(+b.getAttribute('data-remove'), 1); saveCart(c); initCart();
                });
            });
        }
        renderCartTable();
        var co = document.getElementById('checkout-form');
        if (co) co.addEventListener('submit', function (e) {
            e.preventDefault();
            saveCart([]);
            co.innerHTML = '<div class="alert alert-success">🎉 Order placed! A download link has been sent to your email.</div>';
        });
    }

    // "Add to cart" buttons anywhere
    // Guard: page scripts (shop.js, worksheet-page.js, grade-hub.js) bind their
    // own buttons right after rendering, so skip any button already bound to
    // avoid adding the same item twice on one click.
    function initAddToCart() {
        document.querySelectorAll('[data-add-to-cart]').forEach(function (b) {
            if (b.__wwAddBound) return;
            b.__wwAddBound = true;
            b.addEventListener('click', function () {
                var c = cart();
                c.push({
                    title: b.getAttribute('data-title') || 'Worksheet Bundle',
                    meta: b.getAttribute('data-meta') || 'Digital download',
                    price: parseFloat(b.getAttribute('data-price') || '0')
                });
                saveCart(c);
                toast('🛒 Added to cart');
            });
        });
    }

    // Freebie download buttons
    function initFreebies() {
        document.querySelectorAll('[data-freebie]').forEach(function (b) {
            b.addEventListener('click', function () {
                toast('⬇️ Your free PDF is downloading…');
            });
        });
    }

    // FAQ accordion fallback (if Bootstrap JS ever fails)
    function initFaq() {
        var acc = document.querySelector('.faq-accordion');
        if (!acc || typeof bootstrap !== 'undefined') return;
        acc.querySelectorAll('.accordion-button').forEach(function (btn) {
            btn.addEventListener('click', function () {
                var target = document.querySelector(btn.getAttribute('data-bs-target'));
                if (target) target.classList.toggle('show');
                btn.classList.toggle('collapsed');
            });
        });
    }

    onReady(function () {
        initChrome();
        initContact();
        initAuth();
        initCart();
        initAddToCart();
        initFreebies();
        initFaq();
    });

    // Expose cart for shop pages
    window.WWCart = { get: cart, save: saveCart, toast: toast };
})();
