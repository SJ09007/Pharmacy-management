"""Run once to create default admin and staff users."""
from werkzeug.security import generate_password_hash
from app.database import get_db, init_db

init_db()
db = get_db()

users = [
    ('admin', generate_password_hash('admin123'), 'admin'),
    ('staff', generate_password_hash('staff123'), 'staff'),
]

for username, pw_hash, role in users:
    existing = db.execute('SELECT 1 FROM users WHERE username=?', (username,)).fetchone()
    if not existing:
        db.execute('INSERT INTO users (username, password_hash, role) VALUES (?,?,?)', (username, pw_hash, role))

db.commit()
db.close()
print("Seed complete. admin/admin123  staff/staff123")
