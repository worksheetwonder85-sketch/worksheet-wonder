/* Worksheet Wonder — core/payment-gateway.js (demo adapter) */
(function (global) {
    'use strict';
    global.PaymentGateway = {
        // Demo checkout: in production, swap with Stripe/Razorpay SDK calls.
        checkout: function (items) {
            if (global.Logger) global.Logger.info('Demo checkout for', items.length, 'items');
            return new Promise(function (resolve) {
                setTimeout(function () {
                    resolve({ ok: true, orderId: 'WW-' + Date.now(), demo: true });
                }, 800);
            });
        }
    };
})(window);
