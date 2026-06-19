const GST = 0.18;

function calcTotals() {
    let subtotal = 0;
    document.querySelectorAll('.item-row').forEach(row => {
        const sel = row.querySelector('.med-select');
        const qty = parseFloat(row.querySelector('.qty-input').value) || 0;
        const opt = sel.options[sel.selectedIndex];
        const mrp = parseFloat(opt?.dataset.mrp || 0);
        const disc = parseFloat(opt?.dataset.discount || 0);
        const unitPrice = mrp * (1 - disc / 100);
        row.querySelector('.unit-price-display').value = unitPrice > 0 ? '₹' + unitPrice.toFixed(2) : '--';
        subtotal += unitPrice * qty;
    });
    const gst = subtotal * GST;
    document.getElementById('subtotal').textContent = '₹' + subtotal.toFixed(2);
    document.getElementById('gst').textContent = '₹' + gst.toFixed(2);
    document.getElementById('total').textContent = '₹' + (subtotal + gst).toFixed(2);
}

function attachRowEvents(row) {
    row.querySelector('.med-select').addEventListener('change', calcTotals);
    row.querySelector('.qty-input').addEventListener('input', calcTotals);
    row.querySelector('.remove-row').addEventListener('click', () => {
        if (document.querySelectorAll('.item-row').length > 1) { row.remove(); calcTotals(); }
    });
}

document.querySelectorAll('.item-row').forEach(attachRowEvents);

document.getElementById('add-item').addEventListener('click', () => {
    const container = document.getElementById('items-container');
    const first = container.querySelector('.item-row');
    const clone = first.cloneNode(true);
    clone.querySelector('.med-select').value = '';
    clone.querySelector('.qty-input').value = 1;
    clone.querySelector('.unit-price-display').value = '';
    attachRowEvents(clone);
    container.appendChild(clone);
});
