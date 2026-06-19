from flask import Blueprint, render_template, request, redirect, url_for, flash
from ..database import get_db
from ..utils.auth import login_required

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customers_bp.route('/')
@login_required
def index():
    query = request.args.get('q', '')
    db = get_db()
    if query:
        customers = db.execute(
            'SELECT * FROM customers WHERE name LIKE ? OR phone LIKE ?',
            (f'%{query}%', f'%{query}%')
        ).fetchall()
    else:
        customers = db.execute('SELECT * FROM customers ORDER BY customer_id DESC').fetchall()
    db.close()
    return render_template('customers/index.html', customers=customers, query=query)

@customers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        if not name or not phone:
            flash('Name and phone are required.', 'danger')
            return render_template('customers/form.html')
        db = get_db()
        existing = db.execute('SELECT 1 FROM customers WHERE phone = ?', (phone,)).fetchone()
        if existing:
            flash('A customer with this phone number already exists.', 'danger')
            db.close()
            return render_template('customers/form.html')
        db.execute('INSERT INTO customers (name, phone, email) VALUES (?,?,?)', (name, phone, email))
        db.commit()
        db.close()
        flash('Customer added.', 'success')
        return redirect(url_for('customers.index'))
    return render_template('customers/form.html')

@customers_bp.route('/<int:customer_id>')
@login_required
def profile(customer_id):
    db = get_db()
    customer = db.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    bills = db.execute(
        'SELECT * FROM bills WHERE customer_id = ? ORDER BY date DESC', (customer_id,)
    ).fetchall()
    prescriptions = db.execute(
        'SELECT * FROM prescriptions WHERE customer_id = ? ORDER BY date DESC', (customer_id,)
    ).fetchall()
    db.close()
    return render_template('customers/profile.html', customer=customer, bills=bills, prescriptions=prescriptions)
