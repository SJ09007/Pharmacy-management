"""
Populate the database with realistic sample data.
Run: python populate.py
"""
import sqlite3
import random
import os
from datetime import date, timedelta
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'pharmacy.db')

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def random_date(start_days_ago, end_days_ago=0):
    delta = random.randint(end_days_ago, start_days_ago)
    return (date.today() - timedelta(days=delta)).isoformat()

def future_date(days_from_now):
    return (date.today() + timedelta(days=days_from_now)).isoformat()

# ── DATA ────────────────────────────────────────────────────────────────────

MEDICINES = [
    ("Paracetamol 500mg",   "GSK",          "Analgesic",       12.50,  5,  10),
    ("Amoxicillin 250mg",   "Cipla",        "Antibiotic",      45.00,  10, 15),
    ("Metformin 500mg",     "Sun Pharma",   "Antidiabetic",    30.00,  8,  20),
    ("Atorvastatin 10mg",   "Ranbaxy",      "Cardiac",         55.00,  12, 10),
    ("Omeprazole 20mg",     "Dr Reddy",     "Gastro",          25.00,  5,  15),
    ("Cetirizine 10mg",     "Mankind",      "Antihistamine",   8.00,   0,  10),
    ("Azithromycin 500mg",  "Cipla",        "Antibiotic",      85.00,  10, 8),
    ("Amlodipine 5mg",      "Sun Pharma",   "Cardiac",         40.00,  7,  12),
    ("Pantoprazole 40mg",   "Zydus",        "Gastro",          32.00,  5,  10),
    ("Ibuprofen 400mg",     "Abbott",       "Analgesic",       18.00,  5,  15),
    ("Metoprolol 50mg",     "Cipla",        "Cardiac",         48.00,  8,  10),
    ("Losartan 50mg",       "Dr Reddy",     "Cardiac",         52.00,  10, 12),
    ("Glimepiride 2mg",     "Sanofi",       "Antidiabetic",    38.00,  5,  10),
    ("Doxycycline 100mg",   "GSK",          "Antibiotic",      60.00,  10, 8),
    ("Levothyroxine 50mcg", "Abbott",       "Thyroid",         95.00,  5,  5),
    ("Montelukast 10mg",    "MSD",          "Respiratory",     72.00,  8,  10),
    ("Rabeprazole 20mg",    "Eisai",        "Gastro",          28.00,  5,  15),
    ("Clopidogrel 75mg",    "Sun Pharma",   "Cardiac",         65.00,  10, 10),
    ("Vitamin D3 60k",      "Mankind",      "Supplement",      42.00,  0,  20),
    ("Ondansetron 4mg",     "Zydus",        "Antiemetic",      22.00,  5,  15),
    ("Diclofenac 50mg",     "Novartis",     "Analgesic",       14.00,  5,  20),
    ("Tramadol 50mg",       "Cipla",        "Analgesic",       35.00,  0,  10),
    ("Folic Acid 5mg",      "GSK",          "Supplement",      6.00,   0,  25),
    ("Iron Sucrose 100mg",  "Emcure",       "Supplement",      110.00, 5,  8),
    ("Calcium 500mg",       "Cadila",       "Supplement",      20.00,  0,  20),
    ("Aspirin 75mg",        "Bayer",        "Cardiac",         9.00,   0,  30),
    ("Telmisartan 40mg",    "Boehringer",   "Cardiac",         58.00,  10, 10),
    ("Pregabalin 75mg",     "Pfizer",       "Neuropathic",     145.00, 5,  8),
    ("Levocetirizine 5mg",  "UCB",          "Antihistamine",   18.00,  5,  15),
    ("Ranitidine 150mg",    "GSK",          "Gastro",          15.00,  5,  20),
    ("Ciprofloxacin 500mg", "Bayer",        "Antibiotic",      55.00,  10, 10),
    ("Metronidazole 400mg", "Pfizer",       "Antibiotic",      22.00,  5,  15),
    ("Salbutamol Inhaler",  "GSK",          "Respiratory",     135.00, 5,  6),
    ("Insulin Glargine",    "Sanofi",       "Antidiabetic",    980.00, 0,  4),
    ("Warfarin 5mg",        "Abbott",       "Anticoagulant",   48.00,  5,  8),
    ("Furosemide 40mg",     "Sun Pharma",   "Diuretic",        12.00,  0,  20),
    ("Spironolactone 25mg", "Pfizer",       "Diuretic",        28.00,  5,  15),
    ("Allopurinol 300mg",   "Cipla",        "Gout",            24.00,  5,  12),
    ("Sertraline 50mg",     "Pfizer",       "Antidepressant",  85.00,  10, 8),
    ("Alprazolam 0.25mg",   "Pfizer",       "Anxiolytic",      12.00,  5,  10),
    ("Multivitamin",        "Himalaya",     "Supplement",      180.00, 10, 15),
    ("Betahistine 16mg",    "Abbott",       "Vestibular",      65.00,  5,  10),
    ("Aceclofenac 100mg",   "Ipca",         "Analgesic",       22.00,  5,  15),
    ("Pantodac DSR",        "Sun Pharma",   "Gastro",          88.00,  10, 10),
    ("Hydroxychloroquine",  "Ipca",         "Antimalarial",    45.00,  5,  12),
    ("Nifedipine 10mg",     "Bayer",        "Cardiac",         35.00,  5,  10),
    ("Esomeprazole 40mg",   "AstraZeneca",  "Gastro",          75.00,  8,  10),
    ("Terbinafine 250mg",   "Novartis",     "Antifungal",      125.00, 5,  8),
    ("Fluconazole 150mg",   "Pfizer",       "Antifungal",      55.00,  5,  10),
    ("Codeine Phosphate",   "Ranbaxy",      "Analgesic",       28.00,  5,  10),
]

CUSTOMERS = [
    ("Arjun Sharma",    "9876543201", "arjun.sharma@gmail.com"),
    ("Priya Patel",     "9876543202", "priya.patel@yahoo.com"),
    ("Ravi Kumar",      "9876543203", "ravi.kumar@outlook.com"),
    ("Sunita Verma",    "9876543204", "sunita.v@gmail.com"),
    ("Mohan Das",       "9876543205", "mohan.das@gmail.com"),
    ("Kavita Singh",    "9876543206", "kavita.s@hotmail.com"),
    ("Deepak Joshi",    "9876543207", "deepak.j@gmail.com"),
    ("Anita Rao",       "9876543208", "anita.rao@gmail.com"),
    ("Suresh Nair",     "9876543209", "suresh.nair@yahoo.com"),
    ("Meena Pillai",    "9876543210", "meena.p@gmail.com"),
    ("Rajesh Gupta",    "9876543211", "rajesh.gupta@gmail.com"),
    ("Pooja Mehta",     "9876543212", "pooja.m@outlook.com"),
    ("Vikram Chauhan",  "9876543213", "vikram.c@gmail.com"),
    ("Sonia Kapoor",    "9876543214", "sonia.k@gmail.com"),
    ("Anil Tiwari",     "9876543215", "anil.t@yahoo.com"),
    ("Nisha Pandey",    "9876543216", "nisha.p@gmail.com"),
    ("Ramesh Yadav",    "9876543217", "ramesh.y@gmail.com"),
    ("Geeta Mishra",    "9876543218", "geeta.m@hotmail.com"),
    ("Sunil Bhatia",    "9876543219", "sunil.b@gmail.com"),
    ("Rekha Sharma",    "9876543220", "rekha.s@gmail.com"),
    ("Manish Agarwal",  "9876543221", "manish.a@gmail.com"),
    ("Usha Reddy",      "9876543222", "usha.r@yahoo.com"),
    ("Santosh Patil",   "9876543223", "santosh.p@gmail.com"),
    ("Lata Desai",      "9876543224", "lata.d@gmail.com"),
    ("Harish Shah",     "9876543225", "harish.s@outlook.com"),
    ("Vinod Malhotra",  "9876543226", "vinod.m@gmail.com"),
    ("Sudha Menon",     "9876543227", "sudha.m@gmail.com"),
    ("Prakash Iyer",    "9876543228", "prakash.i@yahoo.com"),
    ("Sarla Jain",      "9876543229", "sarla.j@gmail.com"),
    ("Rohit Saxena",    "9876543230", "rohit.s@gmail.com"),
    ("Neha Dubey",      "9876543231", "neha.d@gmail.com"),
    ("Amit Shukla",     "9876543232", "amit.sh@outlook.com"),
    ("Poonam Chandra",  "9876543233", "poonam.c@gmail.com"),
    ("Kiran Bajaj",     "9876543234", "kiran.b@gmail.com"),
    ("Dinesh Kaul",     "9876543235", "dinesh.k@yahoo.com"),
    ("Asha Bhatt",      "9876543236", "asha.b@gmail.com"),
    ("Naresh Trivedi",  "9876543237", "naresh.t@gmail.com"),
    ("Sundar Rajan",    "9876543238", "sundar.r@hotmail.com"),
    ("Lalita Sinha",    "9876543239", "lalita.s@gmail.com"),
    ("Gopal Murthy",    "9876543240", "gopal.m@gmail.com"),
    ("Radha Krishnan",  "9876543241", "radha.k@gmail.com"),
    ("Bharat Wagh",     "9876543242", "bharat.w@yahoo.com"),
    ("Smita Ghosh",     "9876543243", "smita.g@gmail.com"),
    ("Hemant Kulkarni", "9876543244", "hemant.k@gmail.com"),
    ("Indira Nambiar",  "9876543245", "indira.n@outlook.com"),
    ("Tushar Gaikwad",  "9876543246", "tushar.g@gmail.com"),
    ("Varsha Dixit",    "9876543247", "varsha.d@gmail.com"),
    ("Alok Srivastava", "9876543248", "alok.s@gmail.com"),
    ("Padma Venkat",    "9876543249", "padma.v@yahoo.com"),
    ("Chetan Birla",    "9876543250", "chetan.b@gmail.com"),
]

# ── MAIN ────────────────────────────────────────────────────────────────────

def populate():
    db = get_db()

    # -- Init schema
    with open(os.path.join(os.path.dirname(__file__), 'schema.sql')) as f:
        db.executescript(f.read())

    # -- Users
    for username, pw, role in [('admin', 'admin123', 'admin'), ('staff', 'staff123', 'staff')]:
        if not db.execute('SELECT 1 FROM users WHERE username=?', (username,)).fetchone():
            db.execute('INSERT INTO users (username, password_hash, role) VALUES (?,?,?)',
                       (username, generate_password_hash(pw), role))

    # -- Medicines
    med_ids = []
    for row in MEDICINES:
        name = row[0]
        existing = db.execute('SELECT medicine_id FROM medicines WHERE medicine_name=?', (name,)).fetchone()
        if existing:
            med_ids.append(existing['medicine_id'])
        else:
            cur = db.execute(
                'INSERT INTO medicines (medicine_name, manufacturer, category, mrp, discount_percentage, low_stock_threshold) VALUES (?,?,?,?,?,?)',
                row)
            med_ids.append(cur.lastrowid)

    # -- Batches (2-3 per medicine, some expiring soon for dashboard demo)
    batch_counter = 1
    for i, mid in enumerate(med_ids):
        num_batches = random.randint(2, 3)
        for b in range(num_batches):
            # Spread expiry: some near, some far
            if b == 0 and i % 6 == 0:
                exp_days = random.randint(15, 25)   # expiring in 30 days
            elif b == 0 and i % 6 == 1:
                exp_days = random.randint(35, 55)   # expiring in 30-60
            elif b == 0 and i % 6 == 2:
                exp_days = random.randint(65, 85)   # expiring in 60-90
            else:
                exp_days = random.randint(120, 540) # healthy stock
            qty = random.randint(20, 120)
            mfg = future_date(-(exp_days + random.randint(180, 365)))
            exp = future_date(exp_days)
            db.execute(
                'INSERT INTO batches (batch_no, medicine_id, manufacturing_date, expiry_date, quantity) VALUES (?,?,?,?,?)',
                (f'BT{batch_counter:04d}', mid, mfg, exp, qty)
            )
            batch_counter += 1

    # -- Customers
    cust_ids = []
    for name, phone, email in CUSTOMERS:
        existing = db.execute('SELECT customer_id FROM customers WHERE phone=?', (phone,)).fetchone()
        if existing:
            cust_ids.append(existing['customer_id'])
        else:
            cur = db.execute('INSERT INTO customers (name, phone, email) VALUES (?,?,?)', (name, phone, email))
            cust_ids.append(cur.lastrowid)

    # -- Bills + Bill Items (50+ bills spread over last 90 days)
    existing_bills = db.execute('SELECT COUNT(*) as c FROM bills').fetchone()['c']
    if existing_bills == 0:
        for bill_num in range(55):
            cid = random.choice(cust_ids)
            bill_date = random_date(90)
            num_items = random.randint(1, 4)
            chosen_meds = random.sample(list(zip(med_ids, MEDICINES)), num_items)

            subtotal = 0.0
            bill_items = []
            valid = True

            for mid, med_data in chosen_meds:
                qty = random.randint(1, 3)
                avail = db.execute(
                    'SELECT COALESCE(SUM(quantity),0) as s FROM batches WHERE medicine_id=? AND quantity>0', (mid,)
                ).fetchone()['s']
                if avail < qty:
                    valid = False
                    break
                mrp = med_data[3]
                disc = med_data[4]
                unit_price = round(mrp * (1 - disc / 100), 2)
                subtotal += unit_price * qty
                bill_items.append((mid, qty, unit_price))

            if not valid or not bill_items:
                continue

            gst = round(subtotal * 0.18, 2)
            final = round(subtotal + gst, 2)

            cur = db.execute(
                'INSERT INTO bills (customer_id, date, subtotal, gst, final_amount) VALUES (?,?,?,?,?)',
                (cid, bill_date, round(subtotal, 2), gst, final)
            )
            bill_id = cur.lastrowid

            for mid, qty, unit_price in bill_items:
                db.execute(
                    'INSERT INTO bill_items (bill_id, medicine_id, quantity, unit_price) VALUES (?,?,?,?)',
                    (bill_id, mid, qty, unit_price)
                )
                # Deduct FEFO
                remaining = qty
                batches = db.execute(
                    'SELECT * FROM batches WHERE medicine_id=? AND quantity>0 ORDER BY expiry_date ASC', (mid,)
                ).fetchall()
                for batch in batches:
                    if remaining <= 0:
                        break
                    deduct = min(batch['quantity'], remaining)
                    db.execute('UPDATE batches SET quantity=quantity-? WHERE batch_id=?', (deduct, batch['batch_id']))
                    remaining -= deduct

    db.commit()
    db.close()
    print("Done! Populated:")
    print(f"  {len(MEDICINES)} medicines with batches")
    print(f"  {len(CUSTOMERS)} customers")
    print("  ~55 bills with line items")
    print("  Users: admin/admin123  staff/staff123")

if __name__ == '__main__':
    populate()
