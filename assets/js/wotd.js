/* ============================================================
   Worksheet Wonder — Worksheet of the Day (index.html)
   Picks one worksheet per calendar day, deterministically, with
   no backend: index = dayOfYear % WORKSHEETS.length.
   Requires window.WWDatabase (assets/js/database.js) loaded first.
   If the database is missing or empty, the section hides itself
   so the page never looks broken.
   ============================================================ */
(function () {
    'use strict';

    function onReady(fn) {
        if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', fn);
        else fn();
    }

    function esc(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    /* Whole days elapsed since Jan 1 of the current year (local time). */
    function dayOfYear(d) {
        var jan1 = new Date(d.getFullYear(), 0, 1);
        return Math.floor((d - jan1) / 86400000);
    }

    onReady(function () {
        var section = document.getElementById('wotdSection');
        if (!section) return;

        var DB = window.WWDatabase;
        var list = (DB && DB.worksheets) || [];
        if (!list.length) { section.style.display = 'none'; return; }

        var now = new Date();
        var w = list[dayOfYear(now) % list.length];
        if (!w) { section.style.display = 'none'; return; }

        var gradeName = w.grade, subjectName = w.subject;
        try {
            var g = DB.getGradeBySlug(w.grade);
            if (g && g.name) gradeName = g.name;
            var s = DB.getSubjectBySlug(w.subject);
            if (s && s.name) subjectName = s.name;
        } catch (e) { /* fall back to raw slugs */ }

        function set(id, html) {
            var el = document.getElementById(id);
            if (el) el.innerHTML = html;
        }

        var thumb = document.getElementById('wotdThumb');
        if (thumb && w.thumb) {
            thumb.src = w.thumb;
            thumb.alt = w.title;
        }

        set('wotdTitle', esc(w.title));
        set('wotdMeta', esc(w.topic || '') + ' &bull; ' + esc(gradeName) + ' &bull; ' + esc(subjectName));
        set('wotdDate', esc(now.toLocaleDateString('en-GB', {
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric'
        })));

        var btn = document.getElementById('wotdBtn');
        if (btn) btn.href = 'worksheet-details.html?id=' + encodeURIComponent(w.id);
    });
})();
