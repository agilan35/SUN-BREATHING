#!/bin/bash

# Quick Start Script for SUN BREATHING Certificate Detection Platform
# For Linux/macOS systems

echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🔥 SUN BREATHING | Certificate Detection Platform 🔥    ║"
echo "║                                                            ║"
echo "║   Quick Start Setup Script                               ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    echo "   Please install Python 3.8+ using:"
    echo "   - macOS: brew install python3"
    echo "   - Ubuntu/Debian: sudo apt-get install python3"
    exit 1
fi

echo "✓ Python detected:"
python3 --version

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not available"
    exit 1
fi

echo "✓ pip3 is ready"

# Check for Tesseract (optional)
if ! command -v tesseract &> /dev/null; then
    echo ""
    echo "⚠️  Tesseract OCR is not installed (optional)"
    echo "   For better OCR support, install:"
    echo "   - macOS: brew install tesseract"
    echo "   - Ubuntu/Debian: sudo apt-get install tesseract-ocr"
    echo "   - Or use EasyOCR (will be installed automatically)"
    echo ""
else
    echo "✓ Tesseract OCR detected"
fi

# Install dependencies
echo ""
echo "📦 Installing Python dependencies..."
echo "   This may take 2-3 minutes..."
echo ""

pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install dependencies"
    exit 1
fi

echo ""
echo "✓ All dependencies installed successfully!"

# Initialize database
echo ""
echo "🗄️  Initializing database with mock data..."
python3 database.py

echo ""
echo "✓ Database ready!"

# Display next steps
echo ""
echo "╔════════════════════════════════════════════════════════════╗"
echo "║                  ✓ SETUP COMPLETE!                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🚀 To start the server, run:"
echo ""
echo "    python3 app.py"
echo ""
echo "Then open your browser to: http://127.0.0.1:5000"
echo ""
echo "📚 For full documentation, see README.md"
echo ""
echo "Press Ctrl+C to stop the server"
echo ""
