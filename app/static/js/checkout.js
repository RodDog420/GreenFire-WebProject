(function () {
    'use strict';

    const layout  = document.querySelector('[data-stripe-key]');
    if (!layout) return;

    const stripeKey = layout.getAttribute('data-stripe-key');
    const stripe    = Stripe(stripeKey);
    const elements  = stripe.elements();

    // Mount card element
    const cardElement = elements.create('card', {
        style: {
            base: {
                color: '#3E3A35',
                fontFamily: '"DM Sans", sans-serif',
                fontSize: '16px',
                '::placeholder': { color: '#9A9485' }
            },
            invalid: { color: '#C0392B' }
        }
    });
    cardElement.mount('#card-element');

    // Show card validation errors inline
    cardElement.on('change', function (event) {
        const errorEl = document.getElementById('card-error');
        errorEl.textContent = event.error ? event.error.message : '';
    });

    // Fetch PaymentIntent client_secret on page load
    let clientSecret = null;

    fetch('/checkout/create-intent', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'same-origin'
    })
    .then(function (res) { return res.json(); })
    .then(function (data) {
        if (data.error) {
            showError(data.error);
            return;
        }
        clientSecret = data.client_secret;
    })
    .catch(function () {
        showError('Could not connect to payment service. Please refresh and try again.');
    });

    // Handle form submit
    const form       = document.getElementById('checkout-form');
    const submitBtn  = document.getElementById('checkout-submit');
    const processing = document.getElementById('checkout-processing');

    form.addEventListener('submit', function (e) {
        e.preventDefault();

        if (!clientSecret) {
            showError('Payment not ready. Please wait a moment and try again.');
            return;
        }

        setProcessing(true);

        const name = document.getElementById('shipping_name').value;

        stripe.confirmCardPayment(clientSecret, {
            payment_method: {
                card: cardElement,
                billing_details: { name: name }
            }
        })
        .then(function (result) {
            if (result.error) {
                showError(result.error.message);
                setProcessing(false);
            } else if (result.paymentIntent.status === 'succeeded') {
                document.getElementById('payment-intent-id').value =
                    result.paymentIntent.id;
                form.submit();
            }
        });
    });

    function setProcessing(on) {
        submitBtn.disabled  = on;
        processing.textContent = on ? 'Processing payment\u2026' : '';
    }

    function showError(msg) {
        document.getElementById('card-error').textContent = msg;
    }

}());
