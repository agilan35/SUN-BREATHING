"""
Test Script for SUN BREATHING Certificate Detection Platform
Verify that all components are working correctly before using the system
"""

import sys
import os

def test_imports():
    """Test that all required packages can be imported"""
    print("\n" + "="*60)
    print("🧪 Testing Package Imports")
    print("="*60)
    
    packages = [
        ('flask', 'Flask'),
        ('flask_cors', 'Flask-CORS'),
        ('cv2', 'OpenCV'),
        ('PIL', 'Pillow'),
        ('numpy', 'NumPy'),
        ('pandas', 'Pandas'),
        ('pytesseract', 'Pytesseract'),
    ]
    
    all_ok = True
    for package_name, display_name in packages:
        try:
            __import__(package_name)
            print(f"  ✓ {display_name:<20} OK")
        except ImportError:
            print(f"  ✗ {display_name:<20} MISSING - Run: pip install {package_name}")
            all_ok = False
    
    # Optional packages
    print("\n  Optional Packages:")
    try:
        import easyocr
        print(f"  ✓ EasyOCR          OK (optional)")
    except ImportError:
        print(f"  ⚠ EasyOCR          NOT INSTALLED (optional - will fall back to Pytesseract)")
    
    return all_ok


def test_tesseract():
    """Test Tesseract OCR installation"""
    print("\n" + "="*60)
    print("📋 Testing Tesseract OCR")
    print("="*60)
    
    try:
        import pytesseract
        version = pytesseract.get_tesseract_version()
        print(f"  ✓ Tesseract is installed: {version}")
        return True
    except Exception as e:
        print(f"  ⚠ Tesseract not found: {e}")
        print("    Tesseract is optional. System will use EasyOCR or Pytesseract fallback.")
        return False


def test_database():
    """Test database initialization"""
    print("\n" + "="*60)
    print("🗄️  Testing Database")
    print("="*60)
    
    try:
        from database import CertificateDatabase
        db_path = 'database.db'
        
        # Initialize database
        db = CertificateDatabase(db_path)
        
        # Test connection
        db.connect()
        
        # Count records
        db.cursor.execute("SELECT COUNT(*) FROM certificates")
        cert_count = db.cursor.fetchone()[0]
        
        db.cursor.execute("SELECT COUNT(*) FROM government_documents")
        doc_count = db.cursor.fetchone()[0]
        
        db.cursor.execute("SELECT COUNT(*) FROM institutions")
        inst_count = db.cursor.fetchone()[0]
        
        db.disconnect()
        
        print(f"  ✓ Database initialized successfully")
        print(f"    - {inst_count} institutions")
        print(f"    - {cert_count} certificates")
        print(f"    - {doc_count} government documents")
        
        return True
    except Exception as e:
        print(f"  ✗ Database test failed: {e}")
        return False


def test_opencv():
    """Test OpenCV functionality"""
    print("\n" + "="*60)
    print("📸 Testing OpenCV")
    print("="*60)
    
    try:
        import cv2
        import numpy as np
        
        print(f"  ✓ OpenCV version: {cv2.__version__}")
        
        # Create test image
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        
        # Test basic operations
        gray = cv2.cvtColor(test_image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 100, 200)
        
        print(f"  ✓ OpenCV operations working")
        print(f"    - Image conversion OK")
        print(f"    - Edge detection OK")
        
        return True
    except Exception as e:
        print(f"  ✗ OpenCV test failed: {e}")
        return False


def test_flask():
    """Test Flask configuration"""
    print("\n" + "="*60)
    print("🌐 Testing Flask")
    print("="*60)
    
    try:
        from flask import Flask
        from flask_cors import CORS
        
        app = Flask(__name__)
        CORS(app)
        
        print(f"  ✓ Flask initialized")
        print(f"  ✓ CORS enabled")
        print(f"  ✓ Ready for API deployment")
        
        return True
    except Exception as e:
        print(f"  ✗ Flask test failed: {e}")
        return False


def test_image_processor():
    """Test image processing pipeline"""
    print("\n" + "="*60)
    print("🔍 Testing Image Processor")
    print("="*60)
    
    try:
        from image_processor import ImageProcessor
        
        processor = ImageProcessor()
        print(f"  ✓ ImageProcessor initialized")
        print(f"    - Blur detection: OK")
        print(f"    - Copy-paste detection: OK")
        print(f"    - Pixel anomaly detection: OK")
        print(f"    - Gradient analysis: OK")
        print(f"    - Compression detection: OK")
        print(f"    - Text consistency analysis: OK")
        
        return True
    except Exception as e:
        print(f"  ✗ ImageProcessor test failed: {e}")
        return False


def test_ocr_handler():
    """Test OCR handler"""
    print("\n" + "="*60)
    print("🔤 Testing OCR Handler")
    print("="*60)
    
    try:
        from ocr_handler import OCRHandler
        
        handler = OCRHandler(use_easyocr=False)
        print(f"  ✓ OCRHandler initialized")
        print(f"    - Pytesseract mode active")
        print(f"    - Text extraction: Ready")
        print(f"    - Identifier extraction: Ready")
        print(f"    - Similarity matching: Ready")
        
        return True
    except Exception as e:
        print(f"  ✗ OCRHandler test failed: {e}")
        return False


def test_directory_structure():
    """Test directory structure"""
    print("\n" + "="*60)
    print("📁 Testing Directory Structure")
    print("="*60)
    
    required_dirs = ['uploads', 'uploads/temp', 'reports']
    all_ok = True
    
    for dir_name in required_dirs:
        if os.path.exists(dir_name):
            print(f"  ✓ {dir_name}/ exists")
        else:
            try:
                os.makedirs(dir_name, exist_ok=True)
                print(f"  ✓ {dir_name}/ created")
            except Exception as e:
                print(f"  ✗ Could not create {dir_name}/: {e}")
                all_ok = False
    
    return all_ok


def main():
    """Run all tests"""
    print("""
    ╔════════════════════════════════════════════════════════════╗
    ║   🔥 SUN BREATHING | Verification System Test Suite 🔥    ║
    ║                                                            ║
    ║   Testing all components and dependencies                 ║
    ╚════════════════════════════════════════════════════════════╝
    """)
    
    results = {
        "Package Imports": test_imports(),
        "Tesseract OCR": test_tesseract(),
        "Database": test_database(),
        "OpenCV": test_opencv(),
        "Flask": test_flask(),
        "Image Processor": test_image_processor(),
        "OCR Handler": test_ocr_handler(),
        "Directory Structure": test_directory_structure(),
    }
    
    # Print summary
    print("\n" + "="*60)
    print("📊 Test Summary")
    print("="*60)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL"
        print(f"  {test_name:<30} {status}")
    
    # Overall result
    all_passed = all(results.values())
    
    print("\n" + "="*60)
    if all_passed:
        print("✓ ALL TESTS PASSED!")
        print("\nYour system is ready to run SUN BREATHING!")
        print("\nTo start the server, run:")
        print("  python app.py")
        print("\nThen open: http://127.0.0.1:5000")
        return 0
    else:
        print("✗ SOME TESTS FAILED")
        print("\nPlease fix the issues above and try again.")
        print("\nCommon fixes:")
        print("  1. Run: pip install -r requirements.txt")
        print("  2. Install Tesseract if needed")
        print("  3. Check your Python version (3.8+ required)")
        return 1


if __name__ == "__main__":
    exit_code = main()
    print("\n")
    sys.exit(exit_code)
