"""
Configuration file for SUN BREATHING Certificate Detection Platform
Modify these settings to customize the behavior of the system
"""

# ==================== SERVER CONFIGURATION ====================

# Flask server settings
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5000
DEBUG_MODE = True
USE_RELOADER = True

# ==================== FILE UPLOAD CONFIGURATION ====================

# Allowed file extensions
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Maximum file size in bytes (5MB = 5 * 1024 * 1024)
MAX_FILE_SIZE = 5 * 1024 * 1024

# Upload folder paths
UPLOAD_FOLDER = 'uploads'
TEMP_FOLDER = 'uploads/temp'

# ==================== OCR CONFIGURATION ====================

# Choose OCR engine: False = Pytesseract, True = EasyOCR
USE_EASYOCR = False

# Languages to recognize (for EasyOCR)
OCR_LANGUAGES = ['en']

# Image preprocessing for OCR
PREPROCESS_FOR_OCR = True

# ==================== VISUAL INSPECTION THRESHOLDS ====================

# Blur detection (Laplacian variance threshold)
# Higher = more lenient with blur
BLUR_THRESHOLD = 100

# Edge consistency threshold (0-1)
EDGE_THRESHOLD = 0.15

# Color consistency threshold (0-1)
COLOR_CONSISTENCY_THRESHOLD = 0.2

# Gradient variance threshold for inconsistency
GRADIENT_VARIANCE_THRESHOLD = 25

# Compression artifact threshold
COMPRESSION_THRESHOLD = 35

# ==================== VERIFICATION THRESHOLDS ====================

# Overall confidence threshold for REAL verdict (0-100)
# Above this = REAL, Below this = FAKE/SUSPICIOUS
CONFIDENCE_THRESHOLD = 75

# Text match score threshold (0-100)
TEXT_MATCH_THRESHOLD = 70

# Visual score threshold (0-100)
VISUAL_SCORE_THRESHOLD = 60

# Similarity score threshold for name/ID matching (0-100)
SIMILARITY_THRESHOLD = 80

# ==================== DATABASE CONFIGURATION ====================

# Database file path
DATABASE_PATH = 'database.db'

# Auto-initialize database on startup
AUTO_INIT_DATABASE = True

# Pre-load mock data
LOAD_MOCK_DATA = True

# ==================== VERDICT LOGIC ====================

# Critical flags that suggest document is fake
CRITICAL_FLAGS = [
    'COPY_PASTE_DETECTED',
    'PIXEL_ANOMALIES',
    'GRADIENT_INCONSISTENCY'
]

# Warning flags that suggest document is suspicious
WARNING_FLAGS = [
    'BLURRY_IMAGE',
    'COMPRESSION_ARTIFACTS',
    'TEXT_INCONSISTENCY'
]

# ==================== LOGGING & DEBUG ====================

# Enable detailed logging
ENABLE_LOGGING = True

# Log file path (None = console only)
LOG_FILE_PATH = 'verification.log'

# Log level: 'DEBUG', 'INFO', 'WARNING', 'ERROR'
LOG_LEVEL = 'INFO'

# Save verification reports
SAVE_REPORTS = True

# Report output folder
REPORTS_FOLDER = 'reports'

# ==================== CORS CONFIGURATION ====================

# Allow cross-origin requests
ENABLE_CORS = True

# Allowed origins (use '*' for any)
CORS_ORIGINS = '*'

# ==================== PERFORMANCE ====================

# Number of worker threads for Flask
WORKERS = 4

# Enable request caching
ENABLE_CACHE = False

# Cache timeout in seconds
CACHE_TIMEOUT = 300

# ==================== SECURITY ====================

# Enable HTTPS (requires SSL certificate)
USE_HTTPS = False

# SSL certificate path
SSL_CERT_PATH = None

# SSL key path
SSL_KEY_PATH = None

# Rate limiting (requests per minute)
RATE_LIMIT = 60

# ==================== MOCK DATA CONFIGURATION ====================

# Use mock data for testing
USE_MOCK_DATA = True

# Number of mock institutions to create
MOCK_INSTITUTIONS_COUNT = 7

# Number of mock certificates to create
MOCK_CERTIFICATES_COUNT = 5

# Number of mock government documents to create
MOCK_DOCUMENTS_COUNT = 4

# ==================== UI CUSTOMIZATION ====================

# Application name
APP_NAME = "SUN BREATHING"

# Application tagline
APP_TAGLINE = "Fake Certificate & Document Detection Platform"

# Logo image path (relative to static folder)
LOGO_PATH = "logo.png"

# Primary color (hex)
PRIMARY_COLOR = "#B90015"

# Accent color (hex)
ACCENT_COLOR = "#FF98A8"

# Background color (hex)
BG_COLOR = "#0D0D0D"

# ==================== EXPORT & REPORTING ====================

# Enable report export to PDF
EXPORT_PDF = True

# Enable report export to CSV
EXPORT_CSV = True

# Enable report export to JSON
EXPORT_JSON = True

# Default report format ('pdf', 'csv', 'json')
DEFAULT_REPORT_FORMAT = 'json'

# ==================== INTEGRATION SETTINGS ====================

# Enable institution API verification (when implemented)
ENABLE_INSTITUTION_API = False

# Institution API endpoints (example)
INSTITUTION_APIS = {
    'MIT': 'https://api.mit.edu/verify',
    'Stanford': 'https://api.stanford.edu/verify',
}

# Webhook URL for notifications (optional)
WEBHOOK_URL = None

# ==================== ADVANCED SETTINGS ====================

# Enable GPU acceleration (if available)
USE_GPU = False

# OpenCV threading
CV_THREAD_COUNT = 4

# Maximum image dimension for processing
MAX_IMAGE_DIMENSION = 2048

# Minimum image dimension for processing
MIN_IMAGE_DIMENSION = 100

# Image quality threshold (0-100)
MIN_IMAGE_QUALITY = 30
