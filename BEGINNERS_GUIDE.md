# 🚀 BEGINNER'S GUIDE | Getting SUN BREATHING Running

**Welcome!** This guide walks you through setting up and running the SUN BREATHING Certificate Detection Platform from scratch, even if you've never coded before.

---

## ⏱️ Total Setup Time: 10-15 minutes

---

## 📋 Prerequisites Checklist

Before you start, you need:

- ✅ Windows, macOS, or Linux computer
- ✅ Internet connection (for downloading dependencies)
- ✅ Python 3.8 or newer installed
- ✅ About 500MB free disk space
- ✅ A web browser (Chrome, Firefox, Safari, Edge)

---

## 🔧 STEP 1: Install Python (If Needed)

### Check if Python is Already Installed

#### On Windows:
1. Open **Command Prompt** (search "cmd" in Start menu)
2. Type: `python --version`
3. Press Enter

#### On macOS:
1. Open **Terminal** (Applications → Utilities → Terminal)
2. Type: `python3 --version`
3. Press Enter

#### On Linux:
1. Open **Terminal**
2. Type: `python3 --version`
3. Press Enter

**If you see a version number (like "Python 3.9.0"), you're good! Skip to Step 2.**

### If Python is NOT Installed

1. Go to https://www.python.org/downloads/
2. Download the latest Python version (3.11 or newer recommended)
3. Run the installer
4. **IMPORTANT**: Check the box "Add Python to PATH"
5. Click "Install Now"
6. Wait for installation to complete

**Verify installation**: Run `python --version` in Command Prompt again

---

## 📦 STEP 2: Navigate to Your Project Folder

### On Windows:
1. Open **Command Prompt** or **PowerShell**
2. Type: `cd d:\trial`
3. Press Enter
4. You should see `d:\trial>` prompt

### On macOS/Linux:
1. Open **Terminal**
2. Type: `cd ~/trial` (or wherever you saved the project)
3. Press Enter

---

## 📥 STEP 3: Install Dependencies

### Simple Method (Recommended):

#### On Windows:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```

#### On macOS/Linux:
```
python3 -m pip install --upgrade pip
pip3 install -r requirements.txt
```

**What this does**: Downloads and installs Flask, OpenCV, OCR tools, and other packages needed for the system.

**Time**: 2-3 minutes. Your screen will show lots of progress messages. This is normal.

**Common messages you'll see**:
```
Collecting flask==2.3.2
Installing collected packages: flask, opencv-python, pytesseract...
Successfully installed flask-2.3.2 opencv-python-4.8.0.76 ...
```

✅ **If you see "Successfully installed", you're good!**

❌ **If you see errors**: Most common fixes:
```
# Upgrade pip
python -m pip install --upgrade pip

# Then try again
pip install -r requirements.txt

# If still failing, try installing one at a time:
pip install flask
pip install opencv-python
pip install pytesseract
```

---

## 🗄️ STEP 4: Initialize the Database

This creates the SQLite database with pre-loaded certificate and document data.

### On Windows:
```
python database.py
```

### On macOS/Linux:
```
python3 database.py
```

**Expected output**:
```
✓ Mock database successfully initialized with 5 certificates and 4 government documents!

📋 INSTITUTIONS IN DATABASE:
  • Massachusetts Institute of Technology (USA)
  • Stanford University (USA)
  • ...

🎓 CERTIFICATES IN DATABASE:
  • CERT-MIT-2023-001 - Tanjiro Kamado (Advanced Computer Vision)
  • ...

📄 GOVERNMENT DOCUMENTS IN DATABASE:
  • PASSPORT-JP-2023-001 - Tanjiro Kamado (Passport)
  • ...
```

✅ If you see this, the database is ready!

---

## ✅ STEP 5: Verify Everything Works

Run the system test to make sure all components are working:

### On Windows:
```
python test_system.py
```

### On macOS/Linux:
```
python3 test_system.py
```

**Expected output**:
```
✓ Package Imports              PASS
✓ Tesseract OCR               PASS
✓ Database                    PASS
✓ OpenCV                      PASS
✓ Flask                       PASS
✓ Image Processor             PASS
✓ OCR Handler                 PASS
✓ Directory Structure         PASS

✓ ALL TESTS PASSED!
```

⚠️ **If some tests fail**, that's usually OK. Common ones:
- **Tesseract not found**: Optional, system will use fallback OCR
- **EasyOCR not found**: Optional, using Pytesseract instead

As long as you see "Database" and "Flask" pass, you're good!

---

## 🚀 STEP 6: Start the Server

This launches the web application on your computer.

### On Windows:
```
python app.py
```

### On macOS/Linux:
```
python3 app.py
```

**Expected output**:
```
╔════════════════════════════════════════════════════════════╗
║   🔥 SUN BREATHING | Certificate Detection Platform 🔥    ║
║                                                            ║
║   Fake Certificate & Document Detection System            ║
║   Backend API - OpenCV | OCR | Database Verification      ║
╚════════════════════════════════════════════════════════════╝

📊 Initializing components...
   ✓ Database: d:\trial\database.db
   ✓ Upload folder: d:\trial\uploads

🚀 Starting Flask Server...
   → Access at: http://127.0.0.1:5000
   → Frontend: http://127.0.0.1:5000/
   → API: http://127.0.0.1:5000/api/

==============================
WARNING: This is a development server...
Running on http://127.0.0.1:5000
```

✅ **If you see this, the server is running!**

**Do NOT close this terminal window!** Keep it open while you're using the application.

---

## 🌐 STEP 7: Open in Web Browser

1. Open your web browser (Chrome, Firefox, Safari, Edge, etc.)
2. Type in the address bar: `http://127.0.0.1:5000`
3. Press Enter

**You should see**:
- Header with logo "CertVerify"
- "Validate Credentials Instantly" title
- A dark red/crimson colored upload area
- "Drag & Drop your certificate here" text
- A "Scan Document" button

✅ **Congratulations! The system is running!**

---

## 🎯 STEP 8: Test the System

### Create a Test Image

You need a test image to upload. Here are your options:

**Option A: Use a real document**
- Take a clear photo of a certificate, passport, or ID
- Save it as a PNG or JPG file (under 5MB)

**Option B: Use sample text**
- Open Paint, Word, or any text editor
- Type some text (like "CERTIFICATE NAME: John Doe")
- Save as image (PNG or JPG)

**Option C: Download a sample**
- Search Google Images for "certificate template"
- Download and save a certificate image

### Upload and Test

1. On the web page, click the gray upload area
2. Select your image file
3. Click "Scan Document"
4. Watch as the system:
   - Shows "⏳ Analyzing..."
   - Processes the image
   - Extracts text
   - Checks the database
   - Calculates results

5. You'll see a results page with:
   - A verdict (Real/Suspicious/Fake)
   - Extracted text from the image
   - Probability score bars
   - Analysis details

---

## 🛑 STEP 9: Stop the Server

When you're done testing:

1. Go back to the terminal/command prompt
2. Press: **Ctrl + C** (hold Ctrl and press C)
3. You'll see: `^C` or `KeyboardInterrupt`
4. The server will stop

The terminal is now safe to close.

---

## 📁 Your Project Structure

After setup, you should have:

```
d:\trial\
├── index.html                    ← Upload page
├── results.html                  ← Results page
├── style.css                     ← Styling
├── app.py                        ← Main server
├── database.py                   ← Database setup
├── image_processor.py            ← Image analysis
├── ocr_handler.py               ← Text extraction
├── requirements.txt             ← Dependencies list
├── config.py                    ← Configuration
├── test_system.py               ← System tests
├── README.md                    ← Full documentation
├── QUICK_REFERENCE.md           ← Quick tips
├── IMPLEMENTATION_SUMMARY.md    ← What was built
├── database.db                  ← Created after Step 4
└── uploads/                     ← Created automatically
    └── temp/
```

---

## 🎮 Common Commands

### Start the server
```
python app.py              (Windows)
python3 app.py             (macOS/Linux)
```

### Install dependencies
```
pip install -r requirements.txt        (Windows)
pip3 install -r requirements.txt       (macOS/Linux)
```

### Run tests
```
python test_system.py              (Windows)
python3 test_system.py             (macOS/Linux)
```

### Reset database
```
# Delete the database file (optional)
del database.db            (Windows)
rm database.db             (macOS/Linux)

# Recreate it
python database.py         (Windows)
python3 database.py        (macOS/Linux)
```

---

## ⚠️ Troubleshooting

### Error: "Python not found"
**Solution**: 
1. Make sure Python is installed
2. Restart Command Prompt
3. Try: `python --version`

### Error: "Port 5000 in use"
**Solution**:
1. Close other applications using port 5000
2. Or change the port in `app.py` line 228: `port=5001`

### Error: "ModuleNotFoundError: No module named 'flask'"
**Solution**:
```
pip install flask
pip install -r requirements.txt
```

### Error: "Tesseract not found"
**Solution** (Optional - system works without it):
- Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
- macOS: `brew install tesseract`
- Linux: `sudo apt-get install tesseract-ocr`

### The server won't start
**Solution**:
1. Make sure you're in the right folder: `cd d:\trial`
2. Try: `python app.py --debug=False`
3. Check for error messages in the terminal

### Can't see the website
**Solution**:
1. Make sure the server is running (Terminal shows Flask messages)
2. Try: `http://127.0.0.1:5000/` (not https)
3. Try a different browser
4. Clear browser cache (Ctrl+Shift+Del)

---

## 📞 Getting Help

1. **Check the terminal output** - Error messages tell you what's wrong
2. **Read README.md** - Full documentation with explanations
3. **Look at config.py** - Settings you can customize
4. **Run test_system.py** - Tells you what's working/broken

---

## 🎓 What's Happening Behind the Scenes?

### When You Upload an Image:

```
1. FRONTEND (Browser)
   ↓
   You upload an image → Sends to server

2. BACKEND (Python)
   ↓
   File arrives → Saves temporarily

3. VISUAL INSPECTION (OpenCV)
   ↓
   Check: Blur? Artifacts? Edits? Etc.
   Result: Visual Score (0-100)

4. TEXT EXTRACTION (OCR)
   ↓
   Read text from image → Find IDs and names
   Result: Extracted text + Data

5. DATABASE CHECK (SQLite)
   ↓
   Look up data in database → Check for match
   Result: Match score

6. VERDICT (Python Logic)
   ↓
   Combine all scores → Calculate probability
   Result: REAL / SUSPICIOUS / FAKE

7. RESULTS PAGE (Frontend)
   ↓
   Display everything nicely with colors
```

---

## 🎯 Next Steps

Once everything is working:

1. **Experiment**: Upload different images and see results
2. **Customize**: Edit colors in `style.css`
3. **Add Data**: Modify mock data in `database.py`
4. **Learn**: Read the code comments and documentation
5. **Deploy**: Use `config.py` to configure for production

---

## 🏆 You Did It!

You've successfully:
✅ Installed Python and dependencies
✅ Set up the database with mock data
✅ Started the Flask backend server
✅ Accessed the web interface
✅ Tested certificate verification

**You're now a full-stack Python developer!** 🎉

---

## 📚 Additional Resources

- **README.md**: Complete feature documentation
- **QUICK_REFERENCE.md**: Developer quick tips
- **config.py**: All customizable settings
- **IMPLEMENTATION_SUMMARY.md**: Technical architecture
- **In-code comments**: Detailed explanations in Python files

---

## 🔥 Pro Tips

1. **Keep the terminal open** while using the website (it shows you what's happening)
2. **Use JPEG images** for faster processing
3. **Resize large images** before uploading
4. **Test with the mock data** first (names in database)
5. **Check browser console** (F12) for additional information

---

## 🎬 Quick Demo

Want to impress someone? Here's a quick 2-minute demo:

1. Start the server: `python app.py`
2. Open: `http://127.0.0.1:5000`
3. Upload a certificate image
4. Point out:
   - Drag-and-drop interface
   - Real-time analysis
   - Beautiful dark theme
   - Professional results page
   - Color-coded verdicts
5. Explain: "OpenCV analyzes visuals, OCR reads text, SQLite verifies against database"

**Boom!** 🔥 Impressive hackathon project!

---

## ❓ FAQ

**Q: Do I need internet while using it?**
A: No! Everything runs locally on your computer.

**Q: Can I share this with others?**
A: Yes! They need to install Python and dependencies, then run `python app.py`.

**Q: What if I want to add more certificates?**
A: Edit `database.py` and add to the mock data in `populate_mock_data()` function.

**Q: Can I deploy this on a website?**
A: Yes! Use services like Heroku, PythonAnywhere, or AWS. See README.md for details.

**Q: How do I modify the dark theme?**
A: Edit `style.css` and change the hex color codes (e.g., #B90015 for red).

---

**Happy Coding! 🚀 You've got this!**

