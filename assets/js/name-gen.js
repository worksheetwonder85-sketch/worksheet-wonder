/* ============================================================
   Worksheet Wonder — Personalized worksheet generator
   100% client-side: name tracing + spelling word sheets.
   Renders to <canvas id="ng-canvas"> (A4 @ 96dpi: 794 x 1123).
   Dotted trace letters via ctx.setLineDash([3,4]) + strokeText.
   ============================================================ */
(function () {
    'use strict';

    /* ---------- constants ---------- */
    var CANVAS_W = 794;
    var CANVAS_H = 1123;
    var MARGIN = 60;
    var NAVY = '#1F3A5F';
    var ORANGE = '#F26A21';
    var LINE = '#8FA9C7';      // solid ruled lines
    var MIDLINE = '#B9CCE2';   // dashed midline
    var INK = '#33475F';       // dotted letter ink
    var FONT_STACK = '"Baloo 2","Comic Sans MS","Chalkboard SE","Segoe UI",sans-serif';
    var UI_FONT = '"Poppins","Segoe UI",sans-serif';

    /* ---------- state ---------- */
    var canvas = null;
    var ctx = null;
    var mode = 'name';        // 'name' | 'spelling'
    var sizeMode = 'big';     // 'big' | 'small'
    var hasSheet = false;

    function $(id) { return document.getElementById(id); }

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    /* ============================================================
       drawing helpers
       ============================================================ */

    function drawSheetChrome(title, subtitle) {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, CANVAS_W, CANVAS_H);
        ctx.save();
        ctx.textAlign = 'center';
        ctx.fillStyle = NAVY;
        ctx.font = '800 40px ' + FONT_STACK;
        ctx.fillText(title, CANVAS_W / 2, 78);
        ctx.fillStyle = '#5B6B82';
        ctx.font = '500 21px ' + UI_FONT;
        ctx.fillText(subtitle, CANVAS_W / 2, 112);
        ctx.fillStyle = '#8A97A8';
        ctx.font = '500 15px ' + UI_FONT;
        ctx.fillText('Worksheet Wonder  \u2022  Free printable worksheets', CANVAS_W / 2, CANVAS_H - 32);
        ctx.restore();
    }

    /* ruled handwriting set: solid top + baseline, dashed midline */
    function drawRuled(topY, height, x1, x2) {
        if (typeof x1 === 'undefined') x1 = MARGIN;
        if (typeof x2 === 'undefined') x2 = CANVAS_W - MARGIN;
        ctx.save();
        ctx.strokeStyle = LINE;
        ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(x1, topY); ctx.lineTo(x2, topY); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x1, topY + height); ctx.lineTo(x2, topY + height); ctx.stroke();
        ctx.setLineDash([8, 6]);
        ctx.strokeStyle = MIDLINE;
        ctx.beginPath(); ctx.moveTo(x1, topY + height / 2); ctx.lineTo(x2, topY + height / 2); ctx.stroke();
        ctx.restore();
    }

    /* dotted trace letters: light fill + dashed outline */
    function drawDottedText(text, centerX, baselineY, fontSize) {
        ctx.save();
        ctx.font = '800 ' + fontSize + 'px ' + FONT_STACK;
        ctx.textAlign = 'center';
        ctx.textBaseline = 'alphabetic';
        ctx.fillStyle = 'rgba(31,58,95,0.07)';
        ctx.fillText(text, centerX, baselineY);
        ctx.setLineDash([3, 4]);
        ctx.lineWidth = 2.5;
        ctx.strokeStyle = INK;
        ctx.strokeText(text, centerX, baselineY);
        ctx.restore();
    }

    function rowLabel(text, topY) {
        ctx.save();
        ctx.font = '600 19px ' + UI_FONT;
        ctx.fillStyle = ORANGE;
        ctx.textAlign = 'left';
        ctx.textBaseline = 'alphabetic';
        ctx.fillText(text, MARGIN, topY - 12);
        ctx.restore();
    }

    /* shrink font until the text fits maxWidth */
    function fitFont(text, maxWidth, startSize) {
        var size = startSize;
        ctx.font = '800 ' + size + 'px ' + FONT_STACK;
        while (size > 18 && ctx.measureText(text).width > maxWidth) {
            size -= 4;
            ctx.font = '800 ' + size + 'px ' + FONT_STACK;
        }
        return size;
    }

    function titleCase(s) {
        return s.toLowerCase().replace(/(^|\s)([a-z])/g, function (m, p1, p2) {
            return p1 + p2.toUpperCase();
        });
    }

    /* ============================================================
       sheet renderers
       ============================================================ */

    function renderName(rawName) {
        var name = titleCase(rawName.trim().replace(/\s+/g, ' '));
        drawSheetChrome('Trace and Write Your Name', 'Trace the dotted letters, then write your name on your own.');

        var big = (sizeMode === 'big') ? 104 : 76;
        var small = (sizeMode === 'big') ? 68 : 52;
        var maxW = CANVAS_W - (MARGIN * 2) - 20;

        // row 1 — trace big
        var r1top = 150, r1h = 150;
        rowLabel('Trace', r1top);
        drawRuled(r1top, r1h);
        drawDottedText(name, CANVAS_W / 2, r1top + r1h - 14, fitFont(name, maxW, big));

        // row 2 — trace smaller
        var r2top = 352, r2h = 104;
        rowLabel('Trace again', r2top);
        drawRuled(r2top, r2h);
        drawDottedText(name, CANVAS_W / 2, r2top + r2h - 12, fitFont(name, maxW, small));

        // rows 3-5 — freehand
        rowLabel('Write it yourself', 512);
        drawRuled(512, 92);
        drawRuled(672, 92);
        drawRuled(832, 92);
    }

    function renderSpelling(words) {
        drawSheetChrome('My Spelling Words', 'Trace each word, then write it on your own.');

        // column headers
        ctx.save();
        ctx.font = '600 19px ' + UI_FONT;
        ctx.fillStyle = ORANGE;
        ctx.textAlign = 'left';
        ctx.fillText('Trace', MARGIN, 152);
        ctx.fillText('Write', 430, 152);
        ctx.restore();

        var startY = 170, rowH = 108;
        var x1 = MARGIN, x2 = CANVAS_W - MARGIN;
        for (var i = 0; i < words.length; i++) {
            var top = startY + i * rowH;
            // number
            ctx.save();
            ctx.font = '600 18px ' + UI_FONT;
            ctx.fillStyle = '#8A97A8';
            ctx.textAlign = 'left';
            ctx.fillText((i + 1) + '.', x1, top + rowH - 12);
            ctx.restore();
            // full-width ruled set; dotted word on the left half, blank right half
            drawRuled(top, rowH, x1, x2);
            drawDottedText(words[i], 225, top + rowH - 12, fitFont(words[i], 280, 56));
        }
    }

    /* ============================================================
       validation + generation
       ============================================================ */

    function showError(msg) {
        var el = $('ng-error');
        el.textContent = msg;
        el.classList.remove('d-none');
    }

    function clearError() {
        var el = $('ng-error');
        el.textContent = '';
        el.classList.add('d-none');
    }

    function collectSpellingWords() {
        var words = [];
        for (var i = 1; i <= 8; i++) {
            var v = $('ng-word-' + i).value.trim();
            if (v) words.push({ n: i, v: v });
        }
        return words;
    }

    function generate() {
        clearError();
        if (mode === 'name') {
            var raw = $('ng-name').value;
            var clean = raw.trim().replace(/\s+/g, ' ');
            if (!clean) { showError('Type your child\u2019s name to make a worksheet.'); return false; }
            if (!/^[A-Za-z ]+$/.test(clean)) { showError('Please use letters and spaces only.'); return false; }
            if (clean.length > 14) { showError('Please keep the name to 14 characters or fewer.'); return false; }
            renderName(clean);
        } else {
            var entered = collectSpellingWords();
            if (!entered.length) { showError('Type at least one spelling word.'); return false; }
            var words = [];
            for (var i = 0; i < entered.length; i++) {
                var w = entered[i];
                if (!/^[A-Za-z]+$/.test(w.v)) { showError('Word ' + w.n + ': please use letters only (no spaces or numbers).'); return false; }
                if (w.v.length > 12) { showError('Word ' + w.n + ': please keep it to 12 letters or fewer.'); return false; }
                words.push(w.v);
            }
            renderSpelling(words);
        }
        hasSheet = true;
        $('print-sheet').classList.add('has-sheet');
        return true;
    }

    /* ============================================================
       UI wiring
       ============================================================ */

    function setMode(next) {
        mode = next;
        $('ng-mode-name').classList.toggle('active', mode === 'name');
        $('ng-mode-spelling').classList.toggle('active', mode === 'spelling');
        $('ng-panel-name').classList.toggle('d-none', mode !== 'name');
        $('ng-panel-spelling').classList.toggle('d-none', mode !== 'spelling');
        clearError();
        // regenerate live if there is already input
        if (mode === 'name' && $('ng-name').value.trim()) generate();
        if (mode === 'spelling' && collectSpellingWords().length) generate();
    }

    function setSize(next) {
        sizeMode = next;
        $('ng-size-big').classList.toggle('active', sizeMode === 'big');
        $('ng-size-small').classList.toggle('active', sizeMode === 'small');
        if (hasSheet && mode === 'name') generate();
    }

    function downloadPNG() {
        if (!generate()) return;
        var a = document.createElement('a');
        a.download = (mode === 'name' ? 'name-worksheet.png' : 'spelling-worksheet.png');
        a.href = canvas.toDataURL('image/png');
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    function printSheet() {
        if (!generate()) return;
        window.print();
    }

    function buildWordInputs() {
        var wrap = $('ng-words');
        var html = '';
        for (var i = 1; i <= 8; i++) {
            html += '<div class="col-6">' +
                '<input id="ng-word-' + i + '" class="form-control" maxlength="12" ' +
                'placeholder="Word ' + i + '" autocomplete="off" aria-label="Spelling word ' + i + '">' +
                '</div>';
        }
        wrap.innerHTML = html;
        for (var j = 1; j <= 8; j++) {
            (function (k) {
                $('ng-word-' + k).addEventListener('input', function () {
                    if (collectSpellingWords().length) generate();
                    else { clearError(); }
                });
            })(j);
        }
    }

    function ensureFonts(done) {
        try {
            if (document.fonts && document.fonts.load) {
                var p = Promise.all([
                    document.fonts.load('800 100px "Baloo 2"'),
                    document.fonts.load('600 20px "Poppins"'),
                    document.fonts.load('500 21px "Poppins"')
                ]);
                p.then(done).catch(done);
                return;
            }
        } catch (e) { /* fall through */ }
        done();
    }

    onReady(function () {
        canvas = $('ng-canvas');
        if (!canvas) return;
        ctx = canvas.getContext('2d');

        buildWordInputs();

        $('ng-mode-name').addEventListener('click', function () { setMode('name'); });
        $('ng-mode-spelling').addEventListener('click', function () { setMode('spelling'); });
        $('ng-size-big').addEventListener('click', function () { setSize('big'); });
        $('ng-size-small').addEventListener('click', function () { setSize('small'); });

        $('ng-name').addEventListener('input', function () {
            if ($('ng-name').value.trim()) generate();
            else { clearError(); }
        });

        $('ng-print').addEventListener('click', printSheet);
        $('ng-download').addEventListener('click', downloadPNG);

        ensureFonts(function () {
            // re-render with proper fonts once they arrive, if a sheet exists
            if (document.fonts && document.fonts.ready) {
                document.fonts.ready.then(function () { if (hasSheet) generate(); });
            }
        });
    });
})();
