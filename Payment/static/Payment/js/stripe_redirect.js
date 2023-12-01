var button = document.getElementById('myButton');
button.addEventListener('click', function() {
    var butValue = button.value;
    fetch(`http://localhost:8000/payment/buy/${butValue}/`)
        .then(response => response.json())
        .then(data => {
            if (data['error']) {
                alert(data['error']);
            } else {
                var stripe = Stripe(data['key']);
                var session_id = data['session_id'];
                stripe.redirectToCheckout({
                    sessionId: session_id
                });
            }
        });
});