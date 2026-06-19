from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from ..database import get_db
from ..utils.auth import login_required
from ..utils.helpers import allowed_file, save_prescription
import datetime

prescriptions_bp = Blueprint('prescriptions', __name__, url_prefix='/prescriptions')

@prescriptions_bp.route('/upload/<int:customer_id>', methods=['GET', 'POST'])
@login_required
def upload(customer_id):
    db = get_db()
    customer = db.execute('SELECT * FROM customers WHERE customer_id = ?', (customer_id,)).fetchone()
    if not customer:
        flash('Customer not found.', 'danger')
        return redirect(url_for('customers.index'))
    if request.method == 'POST':
        file = request.files.get('prescription')
        if not file or file.filename == '':
            flash('No file selected.', 'danger')
            return render_template('prescriptions/upload.html', customer=customer)
        if not allowed_file(file.filename):
            flash('Unsupported file format. Use JPEG, PNG, or PDF.', 'danger')
            return render_template('prescriptions/upload.html', customer=customer)
        filepath = save_prescription(file, current_app.config['UPLOAD_FOLDER'])
        db.execute(
            'INSERT INTO prescriptions (customer_id, date, image_path) VALUES (?,?,?)',
            (customer_id, datetime.date.today().isoformat(), filepath)
        )
        db.commit()
        db.close()
        flash('Prescription uploaded successfully.', 'success')
        return redirect(url_for('customers.profile', customer_id=customer_id))
    db.close()
    return render_template('prescriptions/upload.html', customer=customer)
