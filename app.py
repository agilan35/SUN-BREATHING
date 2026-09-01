"""
SUN BREATHING | Fake Certificate & Document Detection Platform
Complete Flask Backend with OpenCV, OCR, and Database Verification

This backend provides:
- File upload endpoint for certificate/document images
- OpenCV visual inspection pipeline (blur, edge anomalies, pixel stats, compression)
- OCR text extraction and database cross-verification
- Results API with probability scoring & verification logging
- Sample document endpoints for instant 1-click testing
"""

import os
import sys
import uuid
import json
import base64
from datetime import datetime
from io import BytesIO

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from werkzeug.utils import secure_filename

# Configure safe output encoding for Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass
if sys.stderr and hasattr(sys.stderr, 'reconfigure'):
    try:
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Import custom modules
from database import CertificateDatabase
from image_processor import ImageProcessor
from ocr_handler import OCRHandler

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(UPLOAD_FOLDER, 'temp'), exist_ok=True)

app = Flask(__name__, static_folder=BASE_DIR, static_url_path='')
CORS(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

DB_PATH = os.path.join(BASE_DIR, 'database.db')
_db_init = CertificateDatabase(DB_PATH)

image_processor = ImageProcessor()
ocr_handler = OCRHandler(use_easyocr=False)

CONFIDENCE_THRESHOLD = 75


def get_db():
    """Get database connection for current thread"""
    return CertificateDatabase(DB_PATH)


def allowed_file(filename):
    """Check if file has allowed extension"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def image_to_base64(image_path):
    """Convert image to base64 for frontend display"""
    try:
        with open(image_path, 'rb') as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    except Exception as e:
        print(f"[API] Error converting image to base64: {e}")
        return None


def determine_verdict(visual_score, text_score, is_match, flags):
    """
    Determine overall verdict based on analysis results
    """
    critical_flags = ['COPY_PASTE_DETECTED', 'PIXEL_ANOMALIES', 'GRADIENT_INCONSISTENCY']
    has_critical = any(flag in flags for flag in critical_flags)
    avg_score = (visual_score + text_score) / 2.0

    if is_match and avg_score >= 65 and not has_critical:
        return "REAL"
    elif not is_match and (has_critical or avg_score < 50):
        return "FAKE"
    elif has_critical and len(flags) >= 2:
        return "SUSPICIOUS"
    elif avg_score < 40:
        return "FAKE"
    elif avg_score >= 70:
        return "REAL" if is_match else "SUSPICIOUS"
    else:
        return "SUSPICIOUS"


def analyze_and_verify_image(filepath, original_filename="document.jpg"):
    """Core verification pipeline used by file upload and sample tester"""
    # 1. Visual Inspection
    visual_analysis = image_processor.comprehensive_visual_analysis(filepath)
    visual_score = float(visual_analysis['overall_visual_score'])
    visual_flags = list(visual_analysis['flags'])

    # 2. OCR Text Extraction
    extracted_text, ocr_method = ocr_handler.extract_text(filepath)
    extracted_ids = ocr_handler.extract_identifiers(extracted_text)

    # 3. Database Query & Verification
    is_match = False
    matched_record = None
    text_match_score = 0.0
    match_details = {}
    detected_type = "UNKNOWN"
    db_inst = get_db()

    # Search certificates
    if extracted_ids['certificate_ids']:
        for cert_id in extracted_ids['certificate_ids']:
            names_to_try = extracted_ids['names'] if extracted_ids['names'] else [None]
            for name in names_to_try:
                matched_record = db_inst.verify_certificate(cert_id, name)
                if matched_record:
                    detected_type = "CERTIFICATE"
                    break
            if matched_record:
                break

    # Search government documents
    if not matched_record and extracted_ids['document_ids']:
        for doc_id in extracted_ids['document_ids']:
            names_to_try = extracted_ids['names'] if extracted_ids['names'] else [None]
            for name in names_to_try:
                matched_record = db_inst.verify_government_document(doc_id, name)
                if matched_record:
                    detected_type = "GOVERNMENT_DOCUMENT"
                    break
            if matched_record:
                break

    # Search by names or keywords
    if not matched_record and extracted_ids['names']:
        for name in extracted_ids['names']:
            search_results = db_inst.search_by_keywords(name)
            if search_results:
                matched_record = search_results[0]
                detected_type = "CERTIFICATE"
                break

    # If still not matched, try searching for any institution or course keywords
    if not matched_record and extracted_ids['courses']:
        for course in extracted_ids['courses']:
            search_results = db_inst.search_by_keywords(course)
            if search_results:
                matched_record = search_results[0]
                detected_type = "CERTIFICATE"
                break

    if matched_record:
        is_match, text_match_score, match_details = ocr_handler.verify_match(
            extracted_text, 
            matched_record
        )
    else:
        text_match_score = 15.0 if extracted_text else 0.0
        match_details = {"flags": ["UNREGISTERED_CREDENTIAL"]}

    # 4. Final Verdict
    all_flags = list(dict.fromkeys(visual_flags + match_details.get('flags', [])))
    final_verdict = determine_verdict(visual_score, text_match_score, is_match, all_flags)

    # 5. Log verification
    matched_record_id = None
    matched_dict = None
    if matched_record:
        if hasattr(matched_record, 'keys'):
            matched_dict = dict(matched_record)
            matched_record_id = matched_dict.get('id')
        elif isinstance(matched_record, (tuple, list)):
            matched_record_id = matched_record[0]

    db_inst.log_verification(
        image_hash=visual_analysis['image_hash'],
        extracted_text=extracted_text[:1000],
        detected_type=detected_type,
        matched_id=matched_record_id,
        visual_score=visual_score,
        text_score=text_match_score,
        verdict=final_verdict,
        flags=json.dumps(all_flags)
    )

    image_base64 = image_to_base64(filepath)

    if final_verdict == "REAL":
        real_prob = min(99, max(85, int(visual_score * 0.5 + text_match_score * 0.5)))
        susp_prob = max(1, 100 - real_prob - 5)
        fake_prob = max(0, 100 - real_prob - susp_prob)
    elif final_verdict == "SUSPICIOUS":
        susp_prob = min(85, max(60, int(50 + len(all_flags) * 10)))
        real_prob = max(5, int((100 - susp_prob) * 0.4))
        fake_prob = max(5, 100 - susp_prob - real_prob)
    else:
        fake_prob = min(98, max(80, int(100 - text_match_score * 0.4)))
        susp_prob = max(2, (100 - fake_prob) // 2)
        real_prob = max(0, 100 - fake_prob - susp_prob)

    response = {
        "status": "success",
        "verification_id": os.path.basename(filepath),
        "filename": original_filename,
        "timestamp": datetime.now().isoformat(),
        "image_preview": f"data:image/jpeg;base64,{image_base64}" if image_base64 else "",
        "extracted_text": extracted_text,
        "ocr_method": ocr_method,
        "extracted_ids": extracted_ids,
        "detected_type": detected_type,
        "visual_analysis": visual_analysis,
        "database_verification": {
            "is_match": bool(is_match),
            "text_match_score": round(float(text_match_score), 1),
            "match_details": match_details,
            "matched_record": matched_dict
        },
        "is_match": bool(is_match),
        "visual_score": round(float(visual_score), 1),
        "text_match_score": round(float(text_match_score), 1),
        "overall_verdict": final_verdict,
        "flags": all_flags,
        "confidence": {
            "real_probability": real_prob,
            "suspicious_probability": susp_prob,
            "fake_probability": fake_prob
        }
    }
    return response


# ==================== STATIC ROUTES ====================

@app.route('/', methods=['GET'])
def index():
    """Serve frontend upload page"""
    return send_from_directory(BASE_DIR, 'index.html')


@app.route('/style.css', methods=['GET'])
def style():
    """Serve CSS"""
    return send_from_directory(BASE_DIR, 'style.css')


@app.route('/results.html', methods=['GET'])
def results():
    """Serve results page"""
    return send_from_directory(BASE_DIR, 'results.html')


@app.route('/your-logo.png', methods=['GET'])
def logo_png():
    """Serve logo png if requested"""
    if os.path.exists(os.path.join(BASE_DIR, 'your-logo.png')):
        return send_from_directory(BASE_DIR, 'your-logo.png')
    return send_from_directory(BASE_DIR, 'logo.svg', mimetype='image/svg+xml')


@app.route('/logo.svg', methods=['GET'])
def logo_svg():
    """Serve logo SVG"""
    return send_from_directory(BASE_DIR, 'logo.svg', mimetype='image/svg+xml')


@app.route('/uploads/<filename>', methods=['GET'])
def get_upload(filename):
    """Serve uploaded or sample files"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


# ==================== API ENDPOINTS ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "SUN BREATHING Certificate Detection API",
        "version": "1.2.0",
        "tesseract_available": ocr_handler.extract_text_pytesseract is not None,
        "timestamp": datetime.now().isoformat()
    }), 200


@app.route('/api/upload', methods=['POST'])
def upload_document():
    """Upload and verify certificate/document image"""
    try:
        if 'file' not in request.files:
            return jsonify({"status": "error", "error": "No file provided"}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({"status": "error", "error": "No file selected"}), 400

        if not allowed_file(file.filename):
            return jsonify({"status": "error", "error": "Invalid file type. Allowed: PNG, JPG, JPEG, WEBP"}), 400

        filename = f"{uuid.uuid4().hex[:12]}_{secure_filename(file.filename)}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        response = analyze_and_verify_image(filepath, file.filename)
        return jsonify(response), 200

    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500


@app.route('/api/samples', methods=['GET'])
def list_samples():
    """List available sample certificates for testing"""
    sample_files = [
        {
            "id": "real",
            "title": "Verified MIT Certificate",
            "candidate": "Tanjiro Kamado",
            "institution": "MIT",
            "expected": "REAL",
            "filename": "real_certificate_sample.jpg",
            "url": "/uploads/real_certificate_sample.jpg"
        },
        {
            "id": "fake",
            "title": "Forged Harvard Certificate",
            "candidate": "John Smith",
            "institution": "Harvard University",
            "expected": "FAKE",
            "filename": "fake_certificate_sample.jpg",
            "url": "/uploads/fake_certificate_sample.jpg"
        },
        {
            "id": "suspicious",
            "title": "Altered Official Identity Card",
            "candidate": "Jane Doe",
            "institution": "Department of State",
            "expected": "SUSPICIOUS",
            "filename": "suspicious_document_sample.jpg",
            "url": "/uploads/suspicious_document_sample.jpg"
        }
    ]
    return jsonify({"status": "success", "samples": sample_files}), 200


@app.route('/api/verify-sample/<sample_type>', methods=['POST', 'GET'])
def verify_sample(sample_type):
    """Directly verify a sample certificate without file upload"""
    mapping = {
        "real": "real_certificate_sample.jpg",
        "fake": "fake_certificate_sample.jpg",
        "suspicious": "suspicious_document_sample.jpg"
    }
    filename = mapping.get(sample_type.lower())
    if not filename:
        return jsonify({"status": "error", "error": "Invalid sample type"}), 400

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        from generate_test_certificates import create_real_certificate, create_fake_certificate, create_suspicious_document
        if sample_type == "real":
            create_real_certificate()
        elif sample_type == "fake":
            create_fake_certificate()
        else:
            create_suspicious_document()

    try:
        response = analyze_and_verify_image(filepath, filename)
        return jsonify(response), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/database/info', methods=['GET'])
def database_info():
    """Get database statistics"""
    try:
        info = get_db().get_database_info()
        return jsonify({
            "status": "success",
            "data": info
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


@app.route('/api/verification-history', methods=['GET'])
def verification_history():
    """Get recent verification attempts"""
    try:
        limit = request.args.get('limit', 15, type=int)
        history = get_db().get_verification_history(limit)
        return jsonify({
            "status": "success",
            "history": history
        }), 200
    except Exception as e:
        return jsonify({"status": "error", "error": str(e)}), 500


# ==================== ERROR HANDLERS ====================

@app.errorhandler(413)
def file_too_large(e):
    return jsonify({"status": "error", "error": "File too large. Maximum size is 10MB."}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({"status": "error", "error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(e):
    return jsonify({"status": "error", "error": "Internal server error"}), 500


if __name__ == '__main__':
    print("""
    ============================================================
       SUN BREATHING | Certificate & Document Detection Server
       Full-Stack AI Verification Engine
       OpenCV Visual Inspector + OCR + SQLite Cross-Check
    ============================================================
    """)
    print(f"   * Database: {DB_PATH}")
    print(f"   * Uploads:  {UPLOAD_FOLDER}")
    print("   * Listening on: http://127.0.0.1:5000")
    print("   * Frontend:     http://127.0.0.1:5000/")
    print("============================================================\n")

    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        use_reloader=False,
        threaded=True
    )
