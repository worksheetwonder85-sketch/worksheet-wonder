/* Worksheet Wonder — services/user-service.js */
(function (global) {
    'use strict';
    var KEY = 'ww_user';
    function read() {
        try { return JSON.parse(localStorage.getItem(KEY) || 'null'); } catch (e) { return null; }
    }
    // Seed a friendly demo profile on first visit so the portal always renders.
    var user = read();
    if (!user) {
        user = {
            name: 'Explorer',
            email: '',
            plan: 'Free',
            download_history: [
                { title: 'Trace the Letter A', worksheet_id: 'ws-trace-a', downloaded_at: Date.now() - 86400000 * 2 },
                { title: 'Tracing the Number 1 (One)', worksheet_id: 'ws-num-1', downloaded_at: Date.now() - 86400000 * 5 }
            ],
            favorites: ['ws-trace-a', 'ws-color-1']
        };
        try { localStorage.setItem(KEY, JSON.stringify(user)); } catch (e) {}
    }
    global.UserService = {
        getCurrentUser: function () { return read() || user; },
        updateProfile: function (patch) {
            var u = Object.assign({}, this.getCurrentUser(), patch || {});
            try { localStorage.setItem(KEY, JSON.stringify(u)); } catch (e) {}
            return u;
        },
        logout: function () {
            try { localStorage.removeItem(KEY); } catch (e) {}
            location.href = 'login.html';
        }
    };

    // Portal extras: favorites grid + profile form (progressive enhancement)
    document.addEventListener('DOMContentLoaded', function () {
        var u = global.UserService.getCurrentUser();
        var fav = document.getElementById('portal-favorites-grid');
        if (fav && global.WWDatabase && u && u.favorites) {
            var DB = global.WWDatabase;
            var list = u.favorites.map(DB.getWorksheetById).filter(Boolean);
            fav.innerHTML = list.length && window.WW
                ? list.map(window.WW.worksheetCard).join('')
                : '<div class="col-12"><p class="text-muted">No favorites yet — tap the heart on any worksheet to save it here.</p></div>';
        }
        var form = document.getElementById('portal-profile-form');
        if (form && u) {
            var nameInput = form.querySelector('input[name="name"], #portal-name');
            var emailInput = form.querySelector('input[name="email"], #portal-email');
            if (nameInput) nameInput.value = u.name || '';
            if (emailInput) emailInput.value = u.email || '';
            form.addEventListener('submit', function (e) {
                e.preventDefault();
                global.UserService.updateProfile({
                    name: nameInput ? nameInput.value : u.name,
                    email: emailInput ? emailInput.value : u.email
                });
                var ok = form.querySelector('.profile-saved');
                if (!ok) {
                    ok = document.createElement('div');
                    ok.className = 'alert alert-success mt-3 profile-saved';
                    ok.textContent = '✅ Profile saved!';
                    form.appendChild(ok);
                }
            });
        }
    });
})(window);
