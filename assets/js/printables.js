/* Worksheet Wonder — printables helper (certificates + progress charts).
   Handles: default dates, JS-generated chart grids, and print-only cloning
   (the clicked certificate/chart is copied into #ww-print-area and only
   that area is visible in the printed output). */
(function () {
    'use strict';

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    function buildStarGrid(el) {
        var n = parseInt(el.getAttribute('data-stars') || '10', 10);
        var html = '';
        for (var i = 1; i <= n; i++) {
            html += '<div class="ww-star-cell"><div class="ww-star-glyph" aria-hidden="true">\u2606</div>' +
                '<div class="ww-star-num">' + i + '</div></div>';
        }
        el.innerHTML = html;
    }

    function buildBoxGrid(el) {
        var n = parseInt(el.getAttribute('data-boxes') || '20', 10);
        var html = '';
        for (var i = 1; i <= n; i++) {
            html += '<div class="ww-box-cell"><span>' + i + '</span></div>';
        }
        el.innerHTML = html;
    }

    function buildLogTable(tbody) {
        var html = '';
        for (var d = 1; d <= 30; d++) {
            html += '<tr><td class="ww-log-day">' + d + '</td>' +
                '<td class="ww-log-write"></td><td class="ww-log-write"></td>' +
                '<td class="ww-log-star">\u2606</td></tr>';
        }
        tbody.innerHTML = html;
    }

    function printNode(id, landscape) {
        var src = document.getElementById(id);
        var area = document.getElementById('ww-print-area');
        if (!src || !area) return;
        area.innerHTML = '';
        var clone = src.cloneNode(true);
        clone.removeAttribute('id');
        // Replace live inputs with their printed values so the printout is clean.
        var inputs = clone.querySelectorAll('input');
        for (var i = 0; i < inputs.length; i++) {
            var inp = inputs[i];
            var span = document.createElement('span');
            span.className = ('ww-print-val ' + (inp.className || '')).trim();
            span.textContent = inp.value ? inp.value : '\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0\u00A0';
            inp.parentNode.replaceChild(span, inp);
        }
        area.appendChild(clone);
        var pageStyle = null;
        if (landscape) {
            pageStyle = document.createElement('style');
            pageStyle.textContent = '@page { size: landscape; margin: 8mm; }';
            document.head.appendChild(pageStyle);
        }
        document.body.classList.add('ww-printing');
        var done = function () {
            document.body.classList.remove('ww-printing');
            if (pageStyle && pageStyle.parentNode) pageStyle.parentNode.removeChild(pageStyle);
            area.innerHTML = '';
            window.removeEventListener('afterprint', done);
        };
        window.addEventListener('afterprint', done);
        window.print();
        // Fallback cleanup for environments where afterprint never fires.
        setTimeout(function () { if (document.body.classList.contains('ww-printing')) done(); }, 4000);
    }

    onReady(function () {
        var today = new Date().toISOString().slice(0, 10);
        var dates = document.querySelectorAll('input.ww-date-input');
        for (var i = 0; i < dates.length; i++) { if (!dates[i].value) dates[i].value = today; }

        var stars = document.querySelectorAll('[data-stars]');
        for (var s = 0; s < stars.length; s++) buildStarGrid(stars[s]);
        var boxes = document.querySelectorAll('[data-boxes]');
        for (var b = 0; b < boxes.length; b++) buildBoxGrid(boxes[b]);
        var logs = document.querySelectorAll('[data-log-days]');
        for (var l = 0; l < logs.length; l++) buildLogTable(logs[l]);

        var btns = document.querySelectorAll('[data-print-target]');
        for (var k = 0; k < btns.length; k++) {
            (function (btn) {
                btn.addEventListener('click', function () {
                    printNode(btn.getAttribute('data-print-target'),
                        btn.getAttribute('data-landscape') === '1');
                });
            })(btns[k]);
        }
    });
})();
