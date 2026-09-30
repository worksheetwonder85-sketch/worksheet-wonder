/* Worksheet Wonder — shop.js (shop.html) */
(function () {
    'use strict';
    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    onReady(function () {
        var loading = document.getElementById('products-loading');
        var errBox = document.getElementById('products-error');
        function finishLoading() {
            if (loading) loading.style.display = 'none';
        }
        if (!window.WWDatabase || !window.WW) {
            finishLoading();
            if (errBox) errBox.classList.remove('d-none');
            return;
        }
        var DB = window.WWDatabase;
        var grid = document.getElementById('products-grid');
        if (!grid) { finishLoading(); return; }

        function card(p) {
            return '<div class="col-md-6 col-lg-4 mb-4">' +
                '<div class="bundle-card d-flex flex-column h-100">' +
                '<div class="position-relative"><img src="' + p.thumb + '" alt="' + p.title.replace(/"/g, '') + '" loading="lazy" onerror="this.style.display=\'none\'">' +
                '<span class="badge bg-danger position-absolute top-0 end-0 m-2">SAVE ' + Math.round((1 - p.price / p.oldPrice) * 100) + '%</span></div>' +
                '<div class="p-3 d-flex flex-column flex-grow-1">' +
                '<h5 class="fw-bold">' + p.title + '</h5>' +
                '<p class="text-muted small flex-grow-1">' + p.desc + '</p>' +
                '<div class="mb-1">' + window.WW.stars(p.rating) + '</div>' +
                '<small class="text-muted mb-2">📄 ' + p.worksheets + ' worksheets included</small>' +
                '<div class="mb-3"><span class="price">$' + p.price.toFixed(2) + '</span><span class="price-old">$' + p.oldPrice.toFixed(2) + '</span></div>' +
                '<button class="btn btn-rainbow mt-auto" data-add-to-cart data-title="' + p.title.replace(/"/g, '') + '" data-meta="Digital bundle · ' + p.worksheets + ' worksheets" data-price="' + p.price + '"><i class="bi bi-cart-plus me-2"></i>Add to Cart</button>' +
                '</div></div></div>';
        }

        function render(filter) {
            var list = DB.getProducts().filter(function (p) {
                return !filter || p.title.toLowerCase().indexOf(filter) !== -1;
            });
            grid.classList.remove('d-none');
            grid.innerHTML = list.length ? list.map(card).join('') : '';
            if (!list.length && window.WW) window.WW.emptyState(grid, 'No bundles match your search.');
            finishLoading();
            grid.querySelectorAll('[data-add-to-cart]').forEach(function (b) {
                if (b.__wwAddBound) return;
                b.__wwAddBound = true;
                b.addEventListener('click', function () {
                    if (!window.WWCart) return;
                    var c = window.WWCart.get();
                    c.push({ title: b.getAttribute('data-title'), meta: b.getAttribute('data-meta'), price: parseFloat(b.getAttribute('data-price')) });
                    window.WWCart.save(c);
                    window.WWCart.toast('🛒 Added to cart');
                });
            });
        }

        var input = document.getElementById('shop-search-input');
        if (input) {
            var t;
            input.addEventListener('input', function () {
                clearTimeout(t);
                t = setTimeout(function () { render(input.value.trim().toLowerCase()); }, 250);
            });
        }
        render('');
    });
})();
