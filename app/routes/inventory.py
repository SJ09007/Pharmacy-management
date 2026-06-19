from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import get_db
from ..utils.auth import admin_required, login_required

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/')
@login_required
def index():
    query = request.args.get('q', '')
    category = request.args.get('category', '')
    db = get_db()
    sql = '''SELECT m.*, COALESCE(SUM(b.quantity),0) as total_stock
             FROM medicines m
             LEFT JOIN batches b ON m.medicine_id = b.medicine_id AND b.quantity > 0
             WHERE 1=1'''
    params = []
    if query:
        sql += ' AND (m.medicine_name LIKE ? OR m.category LIKE ?)'
        params += [f'%{query}%', f'%{query}%']
    if category:
        sql += ' AND m.category = ?'
        params.append(category)
    sql += ' GROUP BY m.medicine_id'
    medicines = db.execute(sql, params).fetchall()
    categories = db.execute('SELECT DISTINCT category FROM medicines').fetchall()
    db.close()
    return render_template('inventory/index.html', medicines=medicines, categories=categories, query=query)

@inventory_bp.route('/add', methods=['GET', 'POST'])
@admin_required
def add():
    if request.method == 'POST':
        name = request.form.get('medicine_name', '').strip()
        manufacturer = request.form.get('manufacturer', '').strip()
        category = request.form.get('category', '').strip()
        mrp = request.form.get('mrp', '')
        discount = request.form.get('discount_percentage', 0)
        threshold = request.form.get('low_stock_threshold', 10)
        if not name or not mrp:
            flash('Medicine name and MRP are required.', 'danger')
            return render_template('inventory/form.html', action='Add')
        db = get_db()
        db.execute(
            'INSERT INTO medicines (medicine_name, manufacturer, category, mrp, discount_percentage, low_stock_threshold) VALUES (?,?,?,?,?,?)',
            (name, manufacturer, category, mrp, discount, threshold)
        )
        db.commit()
        db.close()
        flash('Medicine added successfully.', 'success')
        return redirect(url_for('inventory.index'))
    return render_template('inventory/form.html', action='Add', medicine=None)

@inventory_bp.route('/edit/<int:medicine_id>', methods=['GET', 'POST'])
@admin_required
def edit(medicine_id):
    db = get_db()
    medicine = db.execute('SELECT * FROM medicines WHERE medicine_id = ?', (medicine_id,)).fetchone()
    if not medicine:
        flash('Medicine not found.', 'danger')
        return redirect(url_for('inventory.index'))
    if request.method == 'POST':
        name = request.form.get('medicine_name', '').strip()
        manufacturer = request.form.get('manufacturer', '').strip()
        category = request.form.get('category', '').strip()
        mrp = request.form.get('mrp', '')
        discount = request.form.get('discount_percentage', 0)
        threshold = request.form.get('low_stock_threshold', 10)
        if not name or not mrp:
            flash('Medicine name and MRP are required.', 'danger')
            return render_template('inventory/form.html', action='Edit', medicine=medicine)
        db.execute(
            'UPDATE medicines SET medicine_name=?, manufacturer=?, category=?, mrp=?, discount_percentage=?, low_stock_threshold=? WHERE medicine_id=?',
            (name, manufacturer, category, mrp, discount, threshold, medicine_id)
        )
        db.commit()
        db.close()
        flash('Medicine updated.', 'success')
        return redirect(url_for('inventory.index'))
    db.close()
    return render_template('inventory/form.html', action='Edit', medicine=medicine)

@inventory_bp.route('/delete/<int:medicine_id>', methods=['POST'])
@admin_required
def delete(medicine_id):
    db = get_db()
    db.execute('DELETE FROM medicines WHERE medicine_id = ?', (medicine_id,))
    db.commit()
    db.close()
    flash('Medicine deleted.', 'success')
    return redirect(url_for('inventory.index'))

@inventory_bp.route('/batches/<int:medicine_id>', methods=['GET', 'POST'])
@admin_required
def batches(medicine_id):
    db = get_db()
    medicine = db.execute('SELECT * FROM medicines WHERE medicine_id = ?', (medicine_id,)).fetchone()
    if request.method == 'POST':
        batch_no = request.form.get('batch_no', '').strip()
        mfg_date = request.form.get('manufacturing_date')
        exp_date = request.form.get('expiry_date')
        qty = request.form.get('quantity')
        if not batch_no or not exp_date or not qty:
            flash('Batch number, expiry date, and quantity are required.', 'danger')
        else:
            db.execute(
                'INSERT INTO batches (batch_no, medicine_id, manufacturing_date, expiry_date, quantity) VALUES (?,?,?,?,?)',
                (batch_no, medicine_id, mfg_date, exp_date, qty)
            )
            db.commit()
            flash('Batch added.', 'success')
    batches = db.execute(
        'SELECT * FROM batches WHERE medicine_id = ? ORDER BY expiry_date ASC', (medicine_id,)
    ).fetchall()
    db.close()
    return render_template('inventory/batches.html', medicine=medicine, batches=batches)
