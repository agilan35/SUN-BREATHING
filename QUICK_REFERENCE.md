# 🔥 QUICK REFERENCE GUIDE | SUN BREATHING Certificate Detection

## ⚡ Quick Start (3 Steps)

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Initialize Database
```bash
python database.py
```

### 3️⃣ Run the Server
```bash
python app.py
```

**Then open**: http://127.0.0.1:5000

---

## 📁 Project Files & What They Do

| File | Purpose | Type |
|------|---------|------|
| `app.py` | Main Flask backend server | Python |
| `database.py` | SQLite database & mock data | Python |
| `image_processor.py` | OpenCV visual inspection | Python |
| `ocr_handler.py` | Text extraction & verification | Python |
| `index.html` | Frontend upload interface | HTML |
| `results.html` | Results display page | HTML |
| `style.css` | Dark Tanjiro flame theme | CSS |
| `requirements.txt` | Python dependencies | TXT |
| `config.py` | Configuration settings | Python |
| `test_system.py` | System verification tests | Python |

---

## 🌐 API Endpoints

### Upload Document
```http
POST /api/upload
Content-Type: multipart/form-data

Body: file=<image_file>
```
**Response**: Verification results (JSON)

### Health Check
```http
GET /api/health
```

### Database Info
```http
GET /api/database/info
```
**Returns**: Institution/Certificate/Document counts

### Verification History
```http
GET /api/verification-history?limit=10
```

---

## 🔍 Verification Pipeline

```
Input Image
    ↓
[Visual Inspection] → OpenCV Analysis → Blur, Artifacts, Pixels
    ↓
[OCR Extraction] → Text Recognition → Extract IDs, Names, Dates
    ↓
[Database Query] → SQLite Lookup → Find Matching Records
    ↓
[Verification] → Similarity Matching → Score Calculation
    ↓
[Verdict] → REAL / SUSPICIOUS / FAKE
    ↓
[Logging] → Save to Database
    ↓
Output Results
```

---

## 📊 Score Ranges

| Score | Interpretation |
|-------|-----------------|
| 90-100 | Excellent |
| 75-89 | Good |
| 60-74 | Acceptable |
| 40-59 | Questionable |
| 0-39 | Poor |

---

## 🎨 Frontend Structure

```
index.html (Upload Page)
├── Header (Logo + Navigation)
├── Hero Section
│   ├── Title & Description
│   ├── Upload Card
│   │   ├── Drag-Drop Zone
│   │   └── Scan Button
│   └── Feature Cards (3x)
└── Footer (Implicit)

results.html (Results Page)
├── Header
├── Main Results
│   ├── Left Column (Analysis)
│   │   ├── Extracted Text
│   │   ├── Verification Results
│   │   ├── Extracted Data
│   │   └── Detection Flags
│   └── Right Column (Preview + Scores)
│       ├── Document Image
│       └── Probability Bars (Real/Suspicious/Fake)
└── Action Buttons
```

---

## 🗄️ Database Schema

### institutions
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT UNIQUE)
- `code` (TEXT UNIQUE)
- `country` (TEXT)
- `verified` (BOOLEAN)

### certificates
- `id` (INTEGER PRIMARY KEY)
- `certificate_id` (TEXT UNIQUE)
- `recipient_name` (TEXT)
- `institution_id` (FOREIGN KEY)
- `course_name` (TEXT)
- `issue_date` (DATE)
- `expiry_date` (DATE)
- `verification_status` (TEXT)

### government_documents
- `id` (INTEGER PRIMARY KEY)
- `document_id` (TEXT UNIQUE)
- `holder_name` (TEXT)
- `document_type` (TEXT)
- `issue_date` (DATE)
- `issuing_authority` (TEXT)
- `country` (TEXT)

### verification_logs
- `id` (INTEGER PRIMARY KEY)
- `image_hash` (TEXT)
- `extracted_text` (TEXT)
- `visual_score` (FLOAT)
- `text_match_score` (FLOAT)
- `overall_verdict` (TEXT)
- `flags` (TEXT - JSON)
- `created_at` (TIMESTAMP)

---

## 🔧 Customization Quick Tips

### Change OCR Engine
```python
# In app.py, line 30:
ocr_handler = OCRHandler(use_easyocr=True)  # Switch to EasyOCR
```

### Adjust Confidence Threshold
```python
# In app.py, line 29:
CONFIDENCE_THRESHOLD = 85  # Higher = stricter
```

### Add Custom Certificate
```python
# In database.py, populate_mock_data():
certificates = [
    ("CERT-CUSTOM-001", "Name Here", 1, "Course Name", 
     "2023-01-01", "2025-01-01", "VERIFIED"),
]
```

### Change Theme Colors
```css
/* In style.css */
--primary-gradient: linear-gradient(135deg, #FF0000, #00FF00);
--bg-dark: #FFFFFF;  /* Change from obsidian to white */
```

---

## 🚀 Performance Optimization

### Reduce Processing Time
1. **Downscale images** before upload (max 1280x720)
2. **Use JPEG format** (better compression)
3. **Enable GPU** in config.py if available
4. **Use EasyOCR** instead of Pytesseract (with GPU)

### Example Image Optimization
```python
from PIL import Image
img = Image.open('certificate.jpg')
img.thumbnail((1280, 720))
img.save('certificate_optimized.jpg')
```

---

## 🐛 Common Issues & Fixes

| Issue | Solution |
|-------|----------|
| `No module named 'cv2'` | `pip install opencv-python` |
| `Tesseract not found` | Install Tesseract or use EasyOCR |
| `Port 5000 in use` | `python app.py --port 5001` |
| `Permission denied (uploads)` | `chmod 755 uploads` |
| `File too large` | Compress to < 5MB or resize image |

---

## 📝 Testing Checklist

- [ ] Run `python test_system.py`
- [ ] All imports pass ✓
- [ ] Database initialized ✓
- [ ] Flask running ✓
- [ ] Upload form visible ✓
- [ ] File upload works ✓
- [ ] Verification completes ✓
- [ ] Results display correctly ✓

---

## 📚 File Format Support

**Supported Image Formats:**
- PNG (.png)
- JPEG (.jpg, .jpeg)

**Max File Size:** 5 MB

**Recommended Format:** JPEG (better compression)

---

## 🎯 Mock Data for Testing

### Test Certificates (Already in Database)
1. **CERT-MIT-2023-001** → Tanjiro Kamado
2. **CERT-MIT-2023-002** → Nezuko Kamado
3. **CERT-MIT-2023-003** → Inosuke Hashibira
4. **CERT-MIT-2022-001** → Zenitsu Agatsuma
5. **CERT-STANFORD-2023-001** → Kanao Tsuyuri

### Test Documents (Already in Database)
1. **PASSPORT-JP-2023-001** → Tanjiro Kamado
2. **DL-IND-2023-001** → Nezuko Kamado
3. **AADHAR-IND-2022-001** → Inosuke Hashibira
4. **VISA-US-2023-001** → Zenitsu Agatsuma

---

## 🔄 Development Workflow

```bash
# 1. Make changes to code
# 2. Test locally
python test_system.py

# 3. Run dev server (auto-reload enabled)
python app.py

# 4. Test in browser
# http://127.0.0.1:5000

# 5. Commit changes
git add .
git commit -m "Update feature"

# 6. Deploy
# Use production server (gunicorn, etc.)
```

---

## 🔐 Security Considerations

✅ **Implemented:**
- File type validation
- File size limits
- Secure filename handling
- Input sanitization
- CORS protection

❌ **Not Implemented (Future):**
- User authentication
- HTTPS/SSL
- Rate limiting
- API key authentication
- Database encryption

---

## 📊 What Each Analysis Checks

### Visual Inspection (6 Checks)
1. **Blur Detection**: Laplacian variance > 100 = Sharp
2. **Copy-Paste**: Edge consistency analysis
3. **Pixel Anomalies**: Channel variance check
4. **Gradient Issues**: Lighting uniformity
5. **Compression**: DCT block analysis
6. **Text Consistency**: Character size variation

### OCR Verification
- Certificate IDs
- Recipient/Holder names
- Dates (multiple formats)
- Email addresses
- Phone numbers
- Institutions
- Course/Document types

### Database Matching
- Exact ID match
- Name similarity (>75%)
- Institution matching
- Date validation
- Overall score calculation

---

## 🎮 Keyboard Shortcuts

| Key | Action |
|-----|--------|
| Ctrl+C | Stop server |
| F5 | Refresh page |
| F12 | Developer tools |
| Ctrl+Shift+I | Inspect element |

---

## 📞 Getting Help

1. **Check Logs**: Terminal output shows errors
2. **Read README.md**: Full documentation
3. **Check config.py**: Adjustable settings
4. **Run test_system.py**: Diagnostic tool
5. **Review Comments**: In-code documentation

---

## 🏆 Pro Tips

1. **Batch Processing**: Modify `app.py` to add batch endpoint
2. **Database Backup**: Periodically save `database.db`
3. **Monitor Logs**: Track verification attempts
4. **Fine-tune Thresholds**: Adjust confidence based on use
5. **Extend Database**: Add real institution data
6. **API Integration**: Connect to real certificate authorities

---

## 🚀 Deployment Checklist

- [ ] Install all dependencies
- [ ] Run test_system.py successfully
- [ ] Configure database.db with real data
- [ ] Update config.py for production
- [ ] Set DEBUG_MODE = False
- [ ] Use gunicorn instead of Flask dev server
- [ ] Set up HTTPS/SSL
- [ ] Configure database backups
- [ ] Test all API endpoints
- [ ] Monitor server performance

---

## 📈 Next Level Enhancements

1. **Machine Learning**: Train fraud detector model
2. **Blockchain**: Add tamper-proof verification
3. **Mobile App**: React Native wrapper
4. **Admin Panel**: Dashboard for management
5. **Real APIs**: Connect to institutions
6. **Analytics**: Track fraud patterns
7. **Notifications**: Email/SMS alerts
8. **Audit Trail**: Complete verification history

---

**Remember**: The faster you test, the better your hack! 🚀

