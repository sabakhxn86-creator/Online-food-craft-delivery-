function showToast(message, type) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast' + (type ? ' ' + type : '');
    setTimeout(function() { toast.classList.add('hidden'); }, 3000);
}

function addToCart(itemId, quantity, btn) {
    const originalText = btn ? btn.textContent : '';
    if (btn) { btn.disabled = true; btn.textContent = '...'; }

    fetch('/api/cart/add', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ item_id: itemId, quantity: quantity || 1 })
    })
    .then(function(r) { return r.json(); })
    .then(function(data) {
        if (data.success) {
            var countEl = document.getElementById('cart-count');
            if (countEl) countEl.textContent = data.cart_count;
            showToast('Added to cart! 🛒', 'success');
        } else {
            showToast('Failed to add item.', 'error');
        }
    })
    .catch(function() { showToast('Something went wrong.', 'error'); })
    .finally(function() {
        if (btn) { btn.disabled = false; btn.textContent = originalText; }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.add-to-cart').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var itemId = parseInt(this.dataset.itemId);
            addToCart(itemId, 1, this);
        });
    });

    fetch('/api/cart-count')
    .then(function(r) { return r.json(); })
    .then(function(data) {
        var countEl = document.getElementById('cart-count');
        if (countEl && data.count !== undefined) {
            countEl.textContent = data.count;
        }
    })
    .catch(function() {});
});
