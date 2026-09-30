/* Worksheet Wonder — worksheet-page.js (worksheet-details.html?id=...) */
(function () {
    'use strict';
    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }
    onReady(function () {
        if (!window.WWDatabase || !window.WW) return;
        var DB = window.WWDatabase;
        var box = document.getElementById('worksheet-details-container');
        if (!box) return;
        var id = (location.search.match(/[?&]id=([^&]+)/) || [])[1];
        id = id ? decodeURIComponent(id) : null;
        var w = (id && DB.getWorksheetById(id)) || DB.getWorksheets({ limit: 1 })[0];
        if (!w) { window.WW.emptyState(box, 'This worksheet could not be found.'); return; }

        var grade = DB.getGradeBySlug(w.grade);
        var subject = DB.getSubjectBySlug(w.subject);
        document.title = w.title + ' | Worksheet Wonder';
        var priceHtml = w.price > 0
            ? '<span class="price fs-3">$' + w.price.toFixed(2) + '</span>'
            : '<span class="badge bg-success fs-6">FREE Download</span>';
        var pdfFile = w.file || 'assets/pdf/alphabet-free.pdf';
        var cta = w.price > 0
            ? '<button class="btn btn-rainbow btn-lg" data-add-to-cart data-title="' + w.title.replace(/"/g, '') + '" data-meta="Digital worksheet · ' + w.pages + ' pages" data-price="' + w.price + '"><i class="bi bi-cart-plus me-2"></i>Add to Cart</button>'
            : '<a class="btn btn-rainbow btn-lg" href="' + pdfFile + '" download><i class="bi bi-download me-2"></i>Download Free PDF</a>';
        var answerKeyBtn = w.answerKey
            ? '<a class="btn btn-outline-success btn-lg" href="' + w.answerKey + '" download><i class="bi bi-key me-2"></i>Answer Key (Free)</a>'
            : '';

        box.innerHTML =
        '<div class="row g-4">' +
            '<div class="col-lg-6">' +
                '<div class="ww-card p-2"><img src="' + w.thumb + '" class="w-100 rounded" style="max-height:420px;object-fit:cover" alt="' + w.title.replace(/"/g, '') + '" onerror="this.style.display=\'none\'"></div>' +
            '</div>' +
            '<div class="col-lg-6">' +
                '<div class="d-flex gap-2 mb-3 flex-wrap">' +
                    (grade ? '<a href="' + grade.slug + '.html" class="badge bg-primary text-decoration-none">' + grade.name + '</a>' : '') +
                    (subject ? '<a href="' + subject.page + '" class="badge bg-info text-dark text-decoration-none">' + subject.name + '</a>' : '') +
                    '<span class="badge bg-light text-dark">' + w.topic + '</span>' +
                    (window.WW.levelBadge ? window.WW.levelBadge(w.level) : '') +
                '</div>' +
                '<h1 class="fw-bold mb-2">' + w.title + '</h1>' +
                '<div class="mb-3">' + window.WW.stars(w.rating) + ' <span class="text-muted">' + w.rating.toFixed(1) + ' · ' + w.downloads.toLocaleString() + ' downloads</span></div>' +
                '<p class="lead text-muted">' + w.desc + '</p>' +
                '<ul class="list-unstyled mb-4">' +
                    '<li class="mb-2">📄 <strong>' + w.pages + ' printable pages</strong> (PDF, A4 & US Letter)</li>' +
                    '<li class="mb-2">🎯 Aligned to early-learning milestones</li>' +
                    '<li class="mb-2">🖨️ Print at home or school — unlimited use</li>' +
                '</ul>' +
                '<div class="d-flex align-items-center gap-3 mb-4">' + priceHtml + '</div>' +
                '<div class="d-flex gap-3 flex-wrap">' + cta + answerKeyBtn +
                '<a href="worksheets.html" class="btn btn-outline-primary btn-lg">Back to Browse</a></div>' +
            '</div>' +
        '</div>' +
        '<div class="mt-5"><h3 class="fw-bold mb-4">You may also like</h3><div class="row" id="related-grid"></div></div>';

        var related = DB.getWorksheets({ subject: w.subject, grade: w.grade, limit: 8 }).filter(function (x) { return x.id !== w.id; }).slice(0, 4);
        var rg = document.getElementById('related-grid');
        if (rg) rg.innerHTML = related.map(window.WW.worksheetCard).join('');

        box.querySelectorAll('[data-add-to-cart]').forEach(function (b) {
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
    });
})();
