from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from ..database import get_db
from ..utils.auth import login_required
import datetime, json

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')

GST_RATE = 0.18

def deduct_fefo(db, medicine_id, quantity_needed):
    """Deduct stock using FEFO (First Expiry First Out). Returns False if insufficient stock."""
    batches = db.execute(
        'SELECT * FROM batches WHERE medicine_id = ? AND quantity > 0 ORDER BY expiry_date ASC',
        (medicine_id,)
    ).fetchall()
    total_available = sum(b['quantity'] for b in batches)
    if total_available < quantity_needed:
        return False
    remaining = quantity_needed
    for batch in batches:
        if remaining <= 0:
            break
        deduct = min(batch['quantity'], remaining)
        db.execute('UPDATE batches SET quantity = quantity - ? WHERE batch_id = ?', (deduct, batch['batch_id']))
        remaining -= deduct
    return True

@billing_bp.route('/new', methods=['GET', 'POST'])
@login_required
def new_bill():
    db = get_db()
    customers = db.execute('SELECT * FROM customers ORDER BY name').fetchall()
    medicines = db.execute(
        '''SELECT m.medicine_id, m.medicine_name, m.mrp, m.discount_percentage,
           COALESCE(SUM(b.quantity),0) as stock
           FROM medicines m LEFT JOIN batches b ON m.medicine_id=b.medicine_id AND b.quantity>0
           GROUP BY m.medicine_id'''
    ).fetchall()

    if request.method == 'POST':
        customer_id = request.form.get('customer_id')
        medicine_ids = request.form.getlist('medicine_id[]')
        quantities = request.form.getlist('quantity[]')

        if not customer_id or not medicine_ids:
            flash('Customer and at least one medicine are required.', 'danger')
            return render_template('billing/new_bill.html', customers=customers, medicines=medicines)

        subtotal = 0
        bill_items = []

        for mid, qty in zip(medicine_ids, quantities):
            qty = int(qty)
            med = db.execute('SELECT * FROM medicines WHERE medicine_id = ?', (mid,)).fetchone()
            avail = db.execute(
                'SELECT COALESCE(SUM(quantity),0) as s FROM batches WHERE medicine_id=? AND quantity>0', (mid,)
            ).fetchone()['s']
            if qty > avail:
                flash(f'Insufficient stock for {med["medicine_name"]}.', 'danger')
                db.close()
                return render_template('billing/new_bill.html', customers=customers, medicines=medicines)
            unit_price = med['mrp'] * (1 - med['discount_percentage'] / 100)
            subtotal += unit_price * qty
            bill_items.append({'medicine_id': mid, 'quantity': qty, 'unit_price': round(unit_price, 2), 'name': med['medicine_name']})

        gst = round(subtotal * GST_RATE, 2)
        final_amount = round(subtotal + gst, 2)
        today = datetime.date.today().isoformat()

        cur = db.execute(
            'INSERT INTO bills (customer_id, date, subtotal, gst, final_amount) VALUES (?,?,?,?,?)',
            (customer_id, today, round(subtotal, 2), gst, final_amount)
        )
        bill_id = cur.lastrowid

        for item in bill_items:
            db.execute(
                'INSERT INTO bill_items (bill_id, medicine_id, quantity, unit_price) VALUES (?,?,?,?)',
                (bill_id, item['medicine_id'], item['quantity'], item['unit_price'])
            )
            deduct_fefo(db, item['medicine_id'], item['quantity'])

        db.commit()
        db.close()
        flash('Bill generated successfully.', 'success')
        return redirect(url_for('billing.view_bill', bill_id=bill_id))

    db.close()
    return render_template('billing/new_bill.html', customers=customers, medicines=medicines)

@billing_bp.route('/view/<int:bill_id>')
@login_required
def view_bill(bill_id):
    db = get_db()
    bill = db.execute(
        'SELECT b.*, c.name as customer_name, c.phone FROM bills b JOIN customers c ON b.customer_id=c.customer_id WHERE b.bill_id=?',
        (bill_id,)
    ).fetchone()
    items = db.execute(
        'SELECT bi.*, m.medicine_name FROM bill_items bi JOIN medicines m ON bi.medicine_id=m.medicine_id WHERE bi.bill_id=?',
        (bill_id,)
    ).fetchall()
    db.close()
    return render_template('billing/view_bill.html', bill=bill, items=items)

@billing_bp.route('/api/bill/<int:bill_id>/json')
@login_required
def bill_json(bill_id):
    db = get_db()
    bill = db.execute('SELECT * FROM bills WHERE bill_id=?', (bill_id,)).fetchone()
    items = db.execute('SELECT * FROM bill_items WHERE bill_id=?', (bill_id,)).fetchall()
    db.close()
    return jsonify({
        'bill': dict(bill),
        'items': [dict(i) for i in items]
    })
