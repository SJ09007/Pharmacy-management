from flask import Blueprint, render_template, jsonify
from ..database import get_db
from ..utils.auth import admin_required, login_required

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/dashboard')
@admin_required
def index():
    db = get_db()
    total_sales = db.execute('SELECT COUNT(*) as c FROM bills').fetchone()['c']
    total_revenue = db.execute('SELECT COALESCE(SUM(final_amount),0) as r FROM bills').fetchone()['r']
    total_customers = db.execute('SELECT COUNT(*) as c FROM customers').fetchone()['c']

    low_stock = db.execute(
        '''SELECT m.medicine_name, m.low_stock_threshold,
           COALESCE(SUM(b.quantity),0) as stock
           FROM medicines m LEFT JOIN batches b ON m.medicine_id=b.medicine_id AND b.quantity>0
           GROUP BY m.medicine_id
           HAVING stock < m.low_stock_threshold'''
    ).fetchall()

    top_medicines = db.execute(
        '''SELECT m.medicine_name, SUM(bi.quantity) as total_sold
           FROM bill_items bi JOIN medicines m ON bi.medicine_id=m.medicine_id
           GROUP BY bi.medicine_id ORDER BY total_sold DESC LIMIT 5'''
    ).fetchall()

    expiry_30 = db.execute(
        "SELECT m.medicine_name, b.batch_no, b.expiry_date FROM batches b JOIN medicines m ON b.medicine_id=m.medicine_id WHERE b.expiry_date <= date('now','+30 days') AND b.quantity > 0 ORDER BY b.expiry_date"
    ).fetchall()
    expiry_60 = db.execute(
        "SELECT m.medicine_name, b.batch_no, b.expiry_date FROM batches b JOIN medicines m ON b.medicine_id=m.medicine_id WHERE b.expiry_date <= date('now','+60 days') AND b.expiry_date > date('now','+30 days') AND b.quantity > 0 ORDER BY b.expiry_date"
    ).fetchall()
    expiry_90 = db.execute(
        "SELECT m.medicine_name, b.batch_no, b.expiry_date FROM batches b JOIN medicines m ON b.medicine_id=m.medicine_id WHERE b.expiry_date <= date('now','+90 days') AND b.expiry_date > date('now','+60 days') AND b.quantity > 0 ORDER BY b.expiry_date"
    ).fetchall()

    db.close()
    return render_template('dashboard/index.html',
        total_sales=total_sales, total_revenue=total_revenue,
        total_customers=total_customers, low_stock=low_stock,
        top_medicines=top_medicines,
        expiry_30=expiry_30, expiry_60=expiry_60, expiry_90=expiry_90
    )

@dashboard_bp.route('/api/revenue/daily')
@admin_required
def daily_revenue():
    db = get_db()
    rows = db.execute(
        "SELECT date, SUM(final_amount) as revenue FROM bills GROUP BY date ORDER BY date DESC LIMIT 30"
    ).fetchall()
    db.close()
    return jsonify({'labels': [r['date'] for r in rows], 'data': [r['revenue'] for r in rows]})

@dashboard_bp.route('/api/revenue/monthly')
@admin_required
def monthly_revenue():
    db = get_db()
    rows = db.execute(
        "SELECT strftime('%Y-%m', date) as month, SUM(final_amount) as revenue FROM bills GROUP BY month ORDER BY month DESC LIMIT 12"
    ).fetchall()
    db.close()
    return jsonify({'labels': [r['month'] for r in rows], 'data': [r['revenue'] for r in rows]})

@dashboard_bp.route('/api/top-medicines')
@admin_required
def top_medicines_api():
    db = get_db()
    rows = db.execute(
        '''SELECT m.medicine_name, SUM(bi.quantity) as total_sold
           FROM bill_items bi JOIN medicines m ON bi.medicine_id=m.medicine_id
           GROUP BY bi.medicine_id ORDER BY total_sold DESC LIMIT 10'''
    ).fetchall()
    db.close()
    return jsonify({'labels': [r['medicine_name'] for r in rows], 'data': [r['total_sold'] for r in rows]})
