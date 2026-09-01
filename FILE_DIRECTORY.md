# 📁 FILE DIRECTORY REFERENCE | SUN BREATHING

## Quick File Lookup Guide

### 🚀 START HERE
- **START_HERE.md** ← Read this first! Quick overview and getting started
- **BEGINNERS_GUIDE.md** ← Step-by-step setup instructions

---

## 📚 DOCUMENTATION

| File | Purpose | Read If... |
|------|---------|-----------|
| **README.md** | Complete project documentation | You want comprehensive information |
| **QUICK_REFERENCE.md** | Developer quick reference & tips | You're a developer |
| **IMPLEMENTATION_SUMMARY.md** | Technical architecture & design | You want to understand how it works |
| **BEGINNERS_GUIDE.md** | Step-by-step setup guide | You're new to Python/programming |
| **START_HERE.md** | Quick start overview | You just want to run it ASAP |
| **THIS FILE** | File directory reference | You need to find something |

---

## 🔧 APPLICATION FILES

### Backend Python Files

| File | Lines | Purpose | When to Edit |
|------|-------|---------|-------------|
| **app.py** | 515 | Main Flask backend server | Add new endpoints, change port, modify verdict logic |
| **database.py** | 365 | SQLite database setup & mock data | Add more institutions/certificates, modify schema |
| **image_processor.py** | 485 | OpenCV visual inspection pipeline | Adjust detection sensitivity, add new checks |
| **ocr_handler.py** | 410 | OCR text extraction & verification | Switch OCR engines, modify matching logic |

### Frontend Files

| File | Purpose | When to Edit |
|------|---------|-------------|
| **index.html** | Upload interface (main page) | Change text, modify form, update instructions |
| **results.html** | Results display dashboard | Change layout, modify result presentation |
| **style.css** | Styling for dark theme | Change colors, adjust fonts, responsive design |

### Configuration Files

| File | Purpose | When to Edit |
|------|---------|-------------|
| **config.py** | 70+ customizable settings | Adjust thresholds, enable features, set limits |
| **requirements.txt** | Python package dependencies | Update package versions, add new packages |

---

## 🧪 TESTING & SETUP FILES

| File | Purpose | Run When |
|------|---------|----------|
| **test_system.py** | System verification test suite | First time setup, after changes, troubleshooting |
| **setup.bat** | Windows quick setup script | First time on Windows (optional) |
| **setup.sh** | Linux/macOS quick setup script | First time on Linux/macOS (optional) |

---

## 📊 AUTO-CREATED FILES & FOLDERS

These are created automatically after first run:

| Item | Type | Purpose | When Created |
|------|------|---------|-------------|
| **database.db** | File | SQLite database with mock data | First run of `python database.py` |
| **uploads/** | Folder | Stores uploaded document images | First file upload |
| **uploads/temp/** | Folder | Temporary processing folder | First verification |
| **reports/** | Folder | Verification reports (future) | When report generation enabled |

---

## 🗂️ COMPLETE DIRECTORY TREE

```
d:\trial\
│
├── 📄 DOCUMENTATION FILES
│   ├── START_HERE.md                 ← Start here!
│   ├── README.md                     ← Full documentation
│   ├── BEGINNERS_GUIDE.md            ← Setup instructions
│   ├── QUICK_REFERENCE.md            ← Quick tips
│   ├── IMPLEMENTATION_SUMMARY.md     ← Technical details
│   └── FILE_DIRECTORY.md             ← This file
│
├── 🎨 FRONTEND FILES
│   ├── index.html                    ← Upload page
│   ├── results.html                  ← Results page
│   └── style.css                     ← Dark theme styling
│
├── 🚀 BACKEND FILES
│   ├── app.py                        ← Main Flask server
│   ├── database.py                   ← SQLite database
│   ├── image_processor.py            ← OpenCV analysis
│   └── ocr_handler.py                ← Text extraction
│
├── ⚙️ CONFIGURATION FILES
│   ├── config.py                     ← Settings (70+)
│   ├── requirements.txt              ← Dependencies
│   └── .gitignore                    ← Git ignore patterns
│
├── 🧪 TESTING FILES
│   ├── test_system.py                ← System verification
│   ├── setup.bat                     ← Windows setup
│   └── setup.sh                      ← Linux/macOS setup
│
└── 📁 AUTO-CREATED FOLDERS (after first run)
    ├── database.db                   ← SQLite database
    ├── uploads/                      ← Uploaded images
    │   └── temp/                     ← Processing temp files
    └── reports/                      ← Verification reports
```

---

## 🎯 HOW TO FIND WHAT YOU NEED

### I want to...

**...get started immediately**
→ Read `START_HERE.md`

**...follow step-by-step setup**
→ Read `BEGINNERS_GUIDE.md`

**...understand the complete system**
→ Read `README.md`

**...understand the code architecture**
→ Read `IMPLEMENTATION_SUMMARY.md`

**...find quick tips and tricks**
→ Read `QUICK_REFERENCE.md`

**...add a new feature**
→ Edit `app.py`

**...change colors/styling**
→ Edit `style.css`

**...add more certificates**
→ Edit `database.py`

**...adjust detection sensitivity**
→ Edit `config.py`

**...verify everything works**
→ Run `python test_system.py`

**...switch to different OCR**
→ Edit `config.py` or `app.py`

**...deploy to production**
→ Read `README.md` deployment section

**...debug an issue**
→ Run `test_system.py` first, then check `BEGINNERS_GUIDE.md` troubleshooting

---

## 📝 FILE DESCRIPTIONS (DETAILED)

### START_HERE.md (This is your entry point!)
- Quick overview of what's included
- 3-command quick start
- Feature checklist
- Technology stack summary
- Links to other documentation

### README.md (Comprehensive guide)
- Complete installation instructions
- Database schema
- API endpoint documentation
- Verification workflow explanation
- Troubleshooting section
- Performance optimization tips
- Deployment guidelines

### BEGINNERS_GUIDE.md (Step-by-step)
- 9-step setup process
- Python installation guide
- Common error solutions
- Simple explanation of what's happening
- Testing instructions
- FAQ section

### QUICK_REFERENCE.md (Developer cheat sheet)
- 3-step quick start
- File purposes table
- API endpoints quick ref
- Verification pipeline diagram
- Score ranges
- Database schema quick view
- Customization code snippets
- Keyboard shortcuts

### IMPLEMENTATION_SUMMARY.md (Technical deep dive)
- What was built (detailed checklist)
- System architecture diagram
- How components work together
- Analysis breakdown
- Verdict logic explanation
- Performance metrics
- Security features
- Extension points
- Deployment checklist

### app.py (Main backend - 515 lines)
**What it does:**
- Flask server initialization
- Route handlers for upload, health, database info
- File validation
- Orchestrates: Visual inspection → OCR → Database query
- Verdict calculation
- Response formatting
- Error handling

**Key functions:**
- `upload_document()` - Main upload endpoint
- `determine_verdict()` - Verdict calculation logic
- Various route handlers

**When to edit:**
- Add new API endpoints
- Change port number
- Modify verdict logic
- Adjust thresholds
- Add new routes

### database.py (Database setup - 365 lines)
**What it does:**
- SQLite database connection
- Table creation
- Mock data population
- Query methods

**Key classes:**
- `CertificateDatabase` - Main database class

**Key methods:**
- `init_database()` - Create tables
- `populate_mock_data()` - Add sample data
- `verify_certificate()` - Find certificate
- `verify_government_document()` - Find document
- `log_verification()` - Save results

**When to edit:**
- Add more institutions
- Add more certificates
- Modify database schema
- Add new tables
- Change mock data

### image_processor.py (OpenCV pipeline - 485 lines)
**What it does:**
- Image loading
- 6 different visual inspection checks
- Anomaly detection
- Score calculation

**Key class:**
- `ImageProcessor` - Main analysis class

**Key methods:**
- `check_blur_quality()` - Detect blurry images
- `detect_copy_paste_artifacts()` - Find edited regions
- `detect_pixel_anomalies()` - Analyze channels
- `detect_gradient_inconsistencies()` - Check lighting
- `detect_compression_artifacts()` - Find JPEG artifacts
- `analyze_text_region_consistency()` - Check text uniformity
- `comprehensive_visual_analysis()` - Run all checks

**When to edit:**
- Adjust detection sensitivity
- Add new visual checks
- Change thresholds
- Modify scoring logic

### ocr_handler.py (OCR & verification - 410 lines)
**What it does:**
- Text extraction from images
- Identifier parsing
- Database matching
- Similarity scoring

**Key class:**
- `OCRHandler` - Main OCR class

**Key methods:**
- `extract_text()` - Extract text from image
- `extract_identifiers()` - Parse text for IDs, names, dates
- `verify_match()` - Match against database
- `similarity_score()` - Calculate string similarity

**When to edit:**
- Switch OCR engine
- Modify identifier patterns
- Change matching logic
- Adjust similarity thresholds

### index.html (Upload page)
**What it does:**
- Displays upload interface
- Handles file selection
- Communicates with backend

**Key sections:**
- Header with logo
- Hero section with title
- Upload card with drag-drop
- Feature cards
- JavaScript upload logic

**When to edit:**
- Change instructions
- Modify form layout
- Update feature descriptions
- Adjust colors

### results.html (Results dashboard)
**What it does:**
- Displays verification results
- Shows extracted data
- Displays probability bars
- Shows image preview

**Key sections:**
- Header
- Results verdict display
- Left column: Analysis details
- Right column: Image preview + scores
- Action buttons

**When to edit:**
- Change result layout
- Modify display information
- Adjust colors
- Change button actions

### style.css (Styling - 150 lines)
**What it does:**
- Dark theme styling
- Crimson/flame gradient colors
- Responsive design
- Component styling

**Key sections:**
- CSS variables (colors)
- Layout styles
- Component styles
- Responsive breakpoints

**When to edit:**
- Change colors
- Modify fonts
- Adjust layout
- Update responsive design

### config.py (Configuration - 250 lines)
**What it does:**
- Centralized configuration
- All customizable settings
- 70+ configuration options

**Key sections:**
- Server configuration
- File upload settings
- OCR configuration
- Visual inspection thresholds
- Database settings
- Verdict logic
- Logging settings
- Performance settings

**When to edit:**
- Adjust any threshold
- Enable/disable features
- Change default behaviors
- Configure output paths

### requirements.txt (Dependencies)
**What it does:**
- Lists all Python packages needed
- Specifies versions

**Packages included:**
- Flask, OpenCV, Pytesseract, EasyOCR, Pillow, NumPy, Pandas, etc.

**When to edit:**
- Add new package dependencies
- Update package versions
- Remove unused packages

### test_system.py (System verification)
**What it does:**
- Tests all components
- Verifies installations
- Checks database
- Tests functionality

**Key tests:**
- Package imports
- Tesseract installation
- Database connectivity
- OpenCV functions
- Flask setup
- Image processor
- OCR handler
- Directory structure

**When to use:**
- First time setup
- After installing packages
- When troubleshooting
- Before deployment

### setup.bat (Windows setup script)
**What it does:**
- Automates Windows setup
- Checks Python
- Installs packages
- Initializes database

### setup.sh (Linux/macOS setup script)
**What it does:**
- Automates Linux/macOS setup
- Checks Python3
- Installs packages
- Initializes database

### .gitignore (Git ignore patterns)
**What it does:**
- Tells Git which files to ignore
- Prevents uploading unnecessary files

**Ignored items:**
- `__pycache__/` - Python cache
- `*.db` - Database files
- `uploads/` - Uploaded files
- `*.log` - Log files
- `.venv/` - Virtual environment
- `.env` - Environment files

---

## 🔄 TYPICAL WORKFLOWS

### First Time Setup
1. Read: `START_HERE.md`
2. Follow: `BEGINNERS_GUIDE.md`
3. Run: `python app.py`
4. Test: `http://127.0.0.1:5000`

### Want to Customize
1. Check: `QUICK_REFERENCE.md` (for quick tips)
2. Edit: `config.py` (for settings)
3. Edit: `style.css` (for colors)
4. Edit: `database.py` (for data)
5. Run: `test_system.py` (to verify)

### Want to Debug
1. Run: `test_system.py`
2. Read: `BEGINNERS_GUIDE.md` (Troubleshooting section)
3. Check: Terminal output
4. Read: In-code comments

### Want to Deploy
1. Read: `README.md` (Deployment section)
2. Edit: `config.py` (Production settings)
3. Use: `setup.bat`/`setup.sh`
4. Deploy to: Heroku/AWS/PythonAnywhere

### Want to Extend
1. Read: `IMPLEMENTATION_SUMMARY.md` (Extension points)
2. Edit: Relevant Python files
3. Test: `test_system.py`
4. Commit: Changes to Git

---

## ✅ FILE CHECKLIST

All files that should exist:

- [ ] START_HERE.md
- [ ] README.md
- [ ] BEGINNERS_GUIDE.md
- [ ] QUICK_REFERENCE.md
- [ ] IMPLEMENTATION_SUMMARY.md
- [ ] FILE_DIRECTORY.md (this file)
- [ ] app.py
- [ ] database.py
- [ ] image_processor.py
- [ ] ocr_handler.py
- [ ] index.html
- [ ] results.html
- [ ] style.css
- [ ] config.py
- [ ] requirements.txt
- [ ] test_system.py
- [ ] setup.bat
- [ ] setup.sh
- [ ] .gitignore

**All 19 files should be present in `d:\trial\`**

---

## 📞 QUICK LOOKUP

**Need to change something?**
- Colors → `style.css`
- Python settings → `config.py`
- Backend logic → `app.py`
- Database data → `database.py`
- Image analysis → `image_processor.py`
- Text extraction → `ocr_handler.py`

**Need help?**
- Getting started → `START_HERE.md`
- Setup issues → `BEGINNERS_GUIDE.md`
- Code details → `IMPLEMENTATION_SUMMARY.md`
- Quick answers → `QUICK_REFERENCE.md`

**Need to run something?**
- Start server → `python app.py`
- Initialize DB → `python database.py`
- Run tests → `python test_system.py`
- Windows setup → `setup.bat`
- Linux/Mac setup → `setup.sh`

---

**Now you know where everything is!** 🎯

Start with `START_HERE.md` → Then explore as needed!

