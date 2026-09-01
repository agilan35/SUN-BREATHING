"""
Database initialization and mock data setup for SUN BREATHING Certificate Detection
Thread-safe implementation for Flask with concurrent requests
"""

import sqlite3
import os
import sys
from datetime import datetime, timedelta
import json
import threading

# Configure safe output encoding for Windows
if sys.stdout and hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

# Thread-local storage for database connections
_thread_local = threading.local()


def get_db_connection(db_path="database.db"):
    """Get thread-safe database connection (one per thread)"""
    if not hasattr(_thread_local, 'connection') or _thread_local.connection is None:
        _thread_local.connection = sqlite3.connect(db_path, check_same_thread=False)
        _thread_local.connection.row_factory = sqlite3.Row
    return _thread_local.connection


class CertificateDatabase:
    def __init__(self, db_path="database.db"):
        self.db_path = db_path
        self.init_database()

    def get_connection(self):
        """Get thread-safe connection"""
        return get_db_connection(self.db_path)

    def init_database(self):
        """Initialize database with tables"""
        conn = self.get_connection()
        cursor = conn.cursor()

        # Create Institutions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS institutions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                code TEXT UNIQUE NOT NULL,
                country TEXT NOT NULL,
                verified BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create Certificates table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS certificates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                certificate_id TEXT UNIQUE NOT NULL,
                recipient_name TEXT NOT NULL,
                institution_id INTEGER NOT NULL,
                course_name TEXT NOT NULL,
                issue_date DATE NOT NULL,
                expiry_date DATE,
                verification_status TEXT DEFAULT 'PENDING',
                credential_hash TEXT,
                security_features TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (institution_id) REFERENCES institutions(id)
            )
        """)

        # Create Government Documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS government_documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                document_id TEXT UNIQUE NOT NULL,
                holder_name TEXT NOT NULL,
                document_type TEXT NOT NULL,
                issue_date DATE NOT NULL,
                expiry_date DATE,
                issuing_authority TEXT NOT NULL,
                country TEXT NOT NULL,
                verification_status TEXT DEFAULT 'PENDING',
                security_features TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        # Create Verification Logs table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS verification_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                uploaded_image_hash TEXT NOT NULL,
                extracted_text TEXT,
                detected_type TEXT,
                matched_record_id INTEGER,
                visual_score FLOAT,
                text_match_score FLOAT,
                overall_verdict TEXT,
                flags TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.commit()
        self.populate_mock_data()

    def populate_mock_data(self):
        """Populate database with mock data"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()

            # Check if institutions already exist
            cursor.execute("SELECT COUNT(*) FROM institutions")
            if cursor.fetchone()[0] == 0:
                institutions = [
                    ("Massachusetts Institute of Technology", "MIT-001", "USA", 1),
                    ("Stanford University", "STANFORD-001", "USA", 1),
                    ("Oxford University", "OXFORD-001", "United Kingdom", 1),
                    ("Cambridge University", "CAMBRIDGE-001", "United Kingdom", 1),
                    ("Tokyo Institute of Technology", "TOKYO-TECH-001", "Japan", 1),
                    ("Indian Institute of Technology Delhi", "IIT-DELHI-001", "India", 1),
                    ("National University of Singapore", "NUS-001", "Singapore", 1),
                ]
                cursor.executemany(
                    "INSERT OR IGNORE INTO institutions (name, code, country, verified) VALUES (?, ?, ?, ?)",
                    institutions
                )

            # Insert / ensure certificates
            today = datetime.now().date()
            certificates = [
                ("CERT-STAN-2026-0042", "Alex Johnson", 2, "Machine Learning & Artificial Intelligence",
                 "2026-01-15", "2029-01-15", "VERIFIED"),
                ("CERT-MIT-2023-001", "Tanjiro Kamado", 1, "Advanced Computer Vision", 
                 (today - timedelta(days=365)).isoformat(), (today + timedelta(days=730)).isoformat(), "VERIFIED"),
                ("CERT-MIT-2023-002", "Nezuko Kamado", 1, "Machine Learning Engineering",
                 (today - timedelta(days=180)).isoformat(), (today + timedelta(days=915)).isoformat(), "VERIFIED"),
                ("CERT-MIT-2023-003", "Inosuke Hashibira", 1, "Cybersecurity Fundamentals",
                 (today - timedelta(days=90)).isoformat(), (today + timedelta(days=1095)).isoformat(), "VERIFIED"),
                ("CERT-MIT-2022-001", "Zenitsu Agatsuma", 1, "Data Science Specialization",
                 (today - timedelta(days=550)).isoformat(), (today + timedelta(days=545)).isoformat(), "VERIFIED"),
                ("CERT-STANFORD-2023-001", "Kanao Tsuyuri", 2, "Artificial Intelligence",
                 (today - timedelta(days=200)).isoformat(), (today + timedelta(days=895)).isoformat(), "VERIFIED"),
            ]

            cursor.executemany(
                """INSERT OR IGNORE INTO certificates 
                   (certificate_id, recipient_name, institution_id, course_name, 
                    issue_date, expiry_date, verification_status) 
                   VALUES (?, ?, ?, ?, ?, ?, ?)""",
                certificates
            )

            # Insert Government Documents
            documents = [
                ("PASS-USA-987654321", "Jane Doe", "PASSPORT", 
                 "2024-05-10", "2034-05-10",
                 "Department of State", "USA", "VERIFIED"),
                ("PASSPORT-JP-2023-001", "Tanjiro Kamado", "PASSPORT", 
                 (today - timedelta(days=365)).isoformat(), (today + timedelta(days=1825)).isoformat(),
                 "Ministry of Foreign Affairs", "Japan", "VERIFIED"),
                ("DL-IND-2023-001", "Nezuko Kamado", "DRIVER_LICENSE",
                 (today - timedelta(days=200)).isoformat(), (today + timedelta(days=2600)).isoformat(),
                 "Regional Transport Office", "India", "VERIFIED"),
                ("AADHAR-IND-2022-001", "Inosuke Hashibira", "AADHAR",
                 (today - timedelta(days=550)).isoformat(), None,
                 "Unique Identification Authority of India", "India", "VERIFIED"),
                ("VISA-US-2023-001", "Zenitsu Agatsuma", "VISA",
                 (today - timedelta(days=100)).isoformat(), (today + timedelta(days=900)).isoformat(),
                 "U.S. Department of State", "USA", "VERIFIED"),
            ]

            cursor.executemany(
                """INSERT OR IGNORE INTO government_documents 
                   (document_id, holder_name, document_type, issue_date, expiry_date,
                    issuing_authority, country, verification_status) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                documents
            )

            conn.commit()
            print("[DB] Mock database records verified and ready.")

        except Exception as e:
            print(f"[DB] Error setting up mock data: {e}")

    def verify_certificate(self, cert_id, recipient_name=None):
        """Verify certificate by ID and optionally recipient name"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if recipient_name:
                cursor.execute(
                    "SELECT c.*, i.name as institution_name FROM certificates c LEFT JOIN institutions i ON c.institution_id = i.id WHERE c.certificate_id = ? AND c.recipient_name LIKE ?",
                    (cert_id, f"%{recipient_name}%")
                )
                res = cursor.fetchone()
                if res:
                    return res
            
            # Fallback to ID match
            cursor.execute(
                "SELECT c.*, i.name as institution_name FROM certificates c LEFT JOIN institutions i ON c.institution_id = i.id WHERE c.certificate_id = ?",
                (cert_id,)
            )
            return cursor.fetchone()
        except Exception as e:
            print(f"[DB] Error verifying certificate: {e}")
            return None

    def verify_government_document(self, doc_id, holder_name=None):
        """Verify government document by ID and optionally holder name"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            if holder_name:
                cursor.execute(
                    "SELECT * FROM government_documents WHERE document_id = ? AND holder_name LIKE ?",
                    (doc_id, f"%{holder_name}%")
                )
                res = cursor.fetchone()
                if res:
                    return res

            cursor.execute(
                "SELECT * FROM government_documents WHERE document_id = ?",
                (doc_id,)
            )
            return cursor.fetchone()
        except Exception as e:
            print(f"[DB] Error verifying government document: {e}")
            return None

    def search_by_keywords(self, keywords, limit=5):
        """Search database by keywords"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            search_term = f"%{keywords}%"
            
            cursor.execute(
                """SELECT c.id, c.certificate_id, c.recipient_name, c.course_name, c.issue_date, 'CERTIFICATE' as doc_type, i.name as institution_name 
                   FROM certificates c 
                   LEFT JOIN institutions i ON c.institution_id = i.id 
                   WHERE c.recipient_name LIKE ? OR c.course_name LIKE ? OR c.certificate_id LIKE ?
                   UNION 
                   SELECT id, document_id as certificate_id, holder_name as recipient_name, document_type as course_name, issue_date, 'GOVERNMENT_DOC' as doc_type, issuing_authority as institution_name 
                   FROM government_documents 
                   WHERE holder_name LIKE ? OR document_id LIKE ?
                   LIMIT ?""",
                (search_term, search_term, search_term, search_term, search_term, limit)
            )
            return cursor.fetchall()
        except Exception as e:
            print(f"[DB] Error searching by keywords: {e}")
            return []

    def log_verification(self, image_hash, extracted_text, detected_type, matched_id, 
                        visual_score, text_score, verdict, flags):
        """Log verification result"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """INSERT INTO verification_logs 
                   (uploaded_image_hash, extracted_text, detected_type, matched_record_id,
                    visual_score, text_match_score, overall_verdict, flags) 
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                (image_hash, extracted_text, detected_type, matched_id, 
                 visual_score, text_score, verdict, flags)
            )
            conn.commit()
            print(f"[DB] Verification logged: Verdict={verdict}, Visual={visual_score:.1f}, Text={text_score:.1f}")
        except Exception as e:
            print(f"[DB] Error logging verification: {e}")

    def get_database_info(self):
        """Get database statistics"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM institutions")
            institutions_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM certificates")
            certificates_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM government_documents")
            documents_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM verification_logs")
            logs_count = cursor.fetchone()[0]
            
            return {
                "institutions": institutions_count,
                "certificates": certificates_count,
                "government_documents": documents_count,
                "verification_logs": logs_count
            }
        except Exception as e:
            print(f"[DB] Error getting database info: {e}")
            return {}

    def get_verification_history(self, limit=10):
        """Get recent verification attempts"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """SELECT id, uploaded_image_hash, extracted_text, detected_type, 
                   matched_record_id, visual_score, text_match_score, overall_verdict, 
                   flags, created_at 
                   FROM verification_logs 
                   ORDER BY created_at DESC 
                   LIMIT ?""",
                (limit,)
            )
            rows = cursor.fetchall()
            results = []
            for row in rows:
                results.append({
                    "id": row["id"],
                    "image_hash": row["uploaded_image_hash"],
                    "extracted_text": row["extracted_text"][:120] if row["extracted_text"] else None,
                    "detected_type": row["detected_type"],
                    "matched_record_id": row["matched_record_id"],
                    "visual_score": row["visual_score"],
                    "text_score": row["text_match_score"],
                    "verdict": row["overall_verdict"],
                    "flags": json.loads(row["flags"]) if row["flags"] else [],
                    "timestamp": row["created_at"]
                })
            return results
        except Exception as e:
            print(f"[DB] Error getting verification history: {e}")
            return []
