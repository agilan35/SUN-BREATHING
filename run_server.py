#!/usr/bin/env python3
"""Simple test script to verify all components load correctly"""

import sys
print("Python version:", sys.version)

try:
    print("1. Testing Flask import...")
    from flask import Flask
    print("   ✓ Flask imported")
except Exception as e:
    print(f"   ✗ Flask error: {e}")
    sys.exit(1)

try:
    print("2. Testing OpenCV import...")
    import cv2
    print("   ✓ OpenCV imported")
except Exception as e:
    print(f"   ✗ OpenCV error: {e}")
    sys.exit(1)

try:
    print("3. Testing database...")
    from database import CertificateDatabase
    db = CertificateDatabase()
    print("   ✓ Database initialized")
except Exception as e:
    print(f"   ✗ Database error: {e}")
    sys.exit(1)

try:
    print("4. Testing image processor...")
    from image_processor import ImageProcessor
    print("   ✓ Image processor loaded")
except Exception as e:
    print(f"   ✗ Image processor error: {e}")
    sys.exit(1)

try:
    print("5. Testing OCR handler...")
    from ocr_handler import OCRHandler
    print("   ✓ OCR handler loaded")
except Exception as e:
    print(f"   ✗ OCR handler error: {e}")
    sys.exit(1)

print("\n✅ All components loaded successfully!")
print("\nStarting Flask server...")
from app import app

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5000, debug=False, use_reloader=False, threaded=True)
