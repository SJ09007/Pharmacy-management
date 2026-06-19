from flask import Blueprint, render_template, request, flash, current_app
from ..database import get_db
from ..utils.auth import login_required
from ..utils.helpers import allowed_file, save_prescription

ocr_bp = Blueprint('ocr', __name__, url_prefix='/ocr')

@ocr_bp.route('/', methods=['GET', 'POST'])
@login_required
def ocr_scan():
    results = []
    if request.method == 'POST':
        file = request.files.get('prescription')
        if not file or not allowed_file(file.filename):
            flash('Please upload a valid image (JPEG or PNG).', 'danger')
            return render_template('ocr/scan.html', results=results)
        filepath = save_prescription(file, current_app.config['UPLOAD_FOLDER'])
        try:
            import easyocr
            reader = easyocr.Reader(['en'], gpu=False)
            raw = reader.readtext(filepath, detail=0)
            tokens = [t.strip() for t in raw if len(t.strip()) > 2]
            db = get_db()
            for token in tokens:
                match = db.execute(
                    'SELECT medicine_name FROM medicines WHERE medicine_name LIKE ? LIMIT 1',
                    (f'%{token}%',)
                ).fetchone()
                results.append({'token': token, 'status': 'Available' if match else 'Not Available'})
            db.close()
        except ImportError:
            flash('EasyOCR is not installed. Run: pip install easyocr', 'warning')
        except Exception as e:
            flash(f'OCR processing failed: {str(e)}. Try a clearer image.', 'danger')
    return render_template('ocr/scan.html', results=results)
