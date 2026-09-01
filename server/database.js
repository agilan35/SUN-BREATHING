const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

const DATA_DIR = path.join(__dirname, '..', 'data');
const DB_FILE = path.join(DATA_DIR, 'database.json');
const UPLOADS_DIR = path.join(__dirname, '..', 'public', 'uploads');

// Ensure directories exist
if (!fs.existsSync(DATA_DIR)) {
    fs.mkdirSync(DATA_DIR, { recursive: true });
}
if (!fs.existsSync(UPLOADS_DIR)) {
    fs.mkdirSync(UPLOADS_DIR, { recursive: true });
}

// Initial seed data
const initialData = {
    users: [
        {
            id: 'user_001',
            name: 'Dr. Alexander Wright',
            email: 'demo@sunbreathing.ai',
            // Hash for 'password123'
            passwordHash: crypto.createHash('sha256').update('password123').digest('hex'),
            role: 'Institution Admin',
            organization: 'Global Academic Verification Board',
            created_at: '2025-08-01T09:00:00.000Z'
        }
    ],
    feature_cards: [
        {
            id: 'feat_1',
            icon_type: 'brain',
            icon_color: '#EF4444',
            title: 'AI Powered',
            description: 'Advanced AI models analyze patterns and detect manipulations.',
            display_order: 1
        },
        {
            id: 'feat_2',
            icon_type: 'shield',
            icon_color: '#F97316',
            title: 'Secure & Private',
            description: 'Your files are encrypted and handled securely. We value your privacy.',
            display_order: 2
        },
        {
            id: 'feat_3',
            icon_type: 'bolt',
            icon_color: '#EF4444',
            title: 'Fast Results',
            description: 'Get results in seconds with high accuracy and reliability.',
            display_order: 3
        }
    ],
    certificates: [
        {
            id: 'cert_001',
            user_id: 'user_001',
            original_filename: 'certificate_001.jpg',
            stored_filename: 'sample_cert_001.jpg',
            file_size: 142850,
            content_type: 'image/jpeg',
            created_at: '2025-08-28T10:30:00.000Z'
        },
        {
            id: 'cert_002',
            user_id: 'user_001',
            original_filename: 'certificate_002.jpg',
            stored_filename: 'sample_cert_002.jpg',
            file_size: 198420,
            content_type: 'image/jpeg',
            created_at: '2025-08-27T16:15:00.000Z'
        },
        {
            id: 'cert_003',
            user_id: 'user_001',
            original_filename: 'certificate_003.jpg',
            stored_filename: 'sample_cert_003.jpg',
            file_size: 165310,
            content_type: 'image/jpeg',
            created_at: '2025-08-26T11:20:00.000Z'
        }
    ],
    scan_history: [
        {
            id: 'scan_001',
            certificate_id: 'cert_001',
            user_id: 'user_001',
            file_name: 'certificate_001.jpg',
            date_time_display: '28 Aug 2025, 10:30 AM',
            analysis_status: 'Completed',
            final_verdict: 'Real Certificate',
            confidence_score: 98.4,
            completed_at: '2025-08-28T10:30:15.000Z',
            detailed_ai_results: {
                verdict: 'Real Certificate',
                is_authentic: true,
                confidence: 98.4,
                overall_risk: 'Low',
                scores: {
                    seal_integrity: 99.2,
                    signature_authenticity: 97.8,
                    font_consistency: 98.5,
                    metadata_integrity: 100.0,
                    error_level_analysis: 96.7
                },
                tamper_zones: [],
                metadata: {
                    institution: 'Stanford University',
                    recipient_name: 'Emily Rose Davis',
                    degree: 'Bachelor of Science in Computer Science',
                    issue_date: 'June 14, 2024',
                    serial_number: 'SU-CS-2024-88492',
                    digital_signature_valid: true,
                    software_used: 'Official Registrar CertPublisher v4.2'
                },
                findings: [
                    'Cryptographic watermark matches official institutional key registry.',
                    'Seal micro-embossing geometry shows zero pixel-level manipulation.',
                    'Signature stroke pressure velocity is consistent with natural pen stroke.',
                    'Error Level Analysis (ELA) confirms uniform compression across all document quadrants.'
                ]
            }
        },
        {
            id: 'scan_002',
            certificate_id: 'cert_002',
            user_id: 'user_001',
            file_name: 'certificate_002.jpg',
            date_time_display: '27 Aug 2025, 04:15 PM',
            analysis_status: 'Completed',
            final_verdict: 'Fake Certificate',
            confidence_score: 94.6,
            completed_at: '2025-08-27T16:15:22.000Z',
            detailed_ai_results: {
                verdict: 'Fake Certificate',
                is_authentic: false,
                confidence: 94.6,
                overall_risk: 'Critical',
                scores: {
                    seal_integrity: 34.2,
                    signature_authenticity: 28.5,
                    font_consistency: 41.0,
                    metadata_integrity: 15.0,
                    error_level_analysis: 22.8
                },
                tamper_zones: [
                    {
                        id: 'tz_1',
                        x: 28,
                        y: 42,
                        width: 44,
                        height: 12,
                        label: 'Recipient Name Overlay',
                        detail: 'Pixel noise level variance detected (89% discrepancy). Font anti-aliasing does not match original template.',
                        severity: 'high'
                    },
                    {
                        id: 'tz_2',
                        x: 68,
                        y: 72,
                        width: 22,
                        height: 20,
                        label: 'Digital Seal Inconsistency',
                        detail: 'Forged seal contour: Compression boundary artifacts indicate stamp was cropped and pasted from external document.',
                        severity: 'critical'
                    },
                    {
                        id: 'tz_3',
                        x: 18,
                        y: 74,
                        width: 32,
                        height: 14,
                        label: 'Signature Stroke Discontinuity',
                        detail: 'Digital copy-paste halo detected with mismatched alpha threshold.',
                        severity: 'high'
                    }
                ],
                metadata: {
                    institution: 'Massachusetts Institute of Technology (MIT)',
                    recipient_name: 'Johnathan C. Doe [FORGED]',
                    degree: 'Master of Artificial Intelligence',
                    issue_date: 'May 20, 2024',
                    serial_number: 'MIT-ENG-2024-99120 [INVALID]',
                    digital_signature_valid: false,
                    software_used: 'Adobe Photoshop 2024 (Windows)'
                },
                findings: [
                    'CRITICAL: Adobe Photoshop edit history detected in EXIF chunk markers.',
                    'CRITICAL: Forged candidate name with mismatched pixel grid and Gaussian blur smoothing.',
                    'ALERT: Official institutional seal lacks authentic golden metallic spectral resonance.',
                    'ALERT: Serial number format does not match the 2024 Registrar schema.'
                ]
            }
        },
        {
            id: 'scan_003',
            certificate_id: 'cert_003',
            user_id: 'user_001',
            file_name: 'certificate_003.jpg',
            date_time_display: '26 Aug 2025, 11:20 AM',
            analysis_status: 'Completed',
            final_verdict: 'Real Certificate',
            confidence_score: 97.1,
            completed_at: '2025-08-26T11:20:10.000Z',
            detailed_ai_results: {
                verdict: 'Real Certificate',
                is_authentic: true,
                confidence: 97.1,
                overall_risk: 'Low',
                scores: {
                    seal_integrity: 98.0,
                    signature_authenticity: 96.5,
                    font_consistency: 99.1,
                    metadata_integrity: 95.0,
                    error_level_analysis: 97.4
                },
                tamper_zones: [],
                metadata: {
                    institution: 'Harvard Medical School',
                    recipient_name: 'Dr. Sarah Lin',
                    degree: 'Doctor of Medicine (M.D.)',
                    issue_date: 'May 28, 2023',
                    serial_number: 'HMS-MD-2023-44120',
                    digital_signature_valid: true,
                    software_used: 'TrueSeal Verified Registrar Suite'
                },
                findings: [
                    'Full cryptographic signature verification passed against HMS Public Ledger.',
                    'Uniform Error Level Analysis across text, border, and embossed insignia.',
                    'Authentic high-resolution rasterization of medical board crest.',
                    'Metadata timestamps correlate with institutional registry timestamp.'
                ]
            }
        }
    ]
};

// Database helper functions
class Database {
    constructor() {
        this.load();
    }

    load() {
        try {
            if (fs.existsSync(DB_FILE)) {
                const raw = fs.readFileSync(DB_FILE, 'utf8');
                this.data = JSON.parse(raw);
            } else {
                this.data = JSON.parse(JSON.stringify(initialData));
                this.save();
            }
        } catch (err) {
            console.error('Error loading DB, resetting to defaults:', err);
            this.data = JSON.parse(JSON.stringify(initialData));
            this.save();
        }
    }

    save() {
        try {
            fs.writeFileSync(DB_FILE, JSON.stringify(this.data, null, 2), 'utf8');
        } catch (err) {
            console.error('Error saving DB:', err);
        }
    }

    // Users
    findUserByEmail(email) {
        return this.data.users.find(u => u.email.toLowerCase() === email.toLowerCase());
    }

    findUserById(id) {
        return this.data.users.find(u => u.id === id);
    }

    createUser(user) {
        const newUser = {
            id: 'user_' + crypto.randomBytes(4).toString('hex'),
            created_at: new Date().toISOString(),
            ...user
        };
        this.data.users.push(newUser);
        this.save();
        return newUser;
    }

    // Features
    getFeatureCards() {
        return [...this.data.feature_cards].sort((a, b) => a.display_order - b.display_order);
    }

    updateFeatureCard(id, updates) {
        const index = this.data.feature_cards.findIndex(f => f.id === id);
        if (index !== -1) {
            this.data.feature_cards[index] = { ...this.data.feature_cards[index], ...updates };
            this.save();
            return this.data.feature_cards[index];
        }
        return null;
    }

    // Scans
    getScans(options = {}) {
        let results = [...this.data.scan_history];

        if (options.userId) {
            // Optional user filter
        }

        if (options.verdict && options.verdict !== 'all') {
            const target = options.verdict.toLowerCase();
            results = results.filter(s => {
                if (target === 'real') return s.final_verdict.toLowerCase().includes('real');
                if (target === 'fake') return s.final_verdict.toLowerCase().includes('fake');
                return true;
            });
        }

        if (options.search) {
            const q = options.search.toLowerCase();
            results = results.filter(s =>
                s.file_name.toLowerCase().includes(q) ||
                (s.detailed_ai_results && s.detailed_ai_results.metadata &&
                    (s.detailed_ai_results.metadata.institution.toLowerCase().includes(q) ||
                     s.detailed_ai_results.metadata.recipient_name.toLowerCase().includes(q)))
            );
        }

        // Sort: default newest first
        results.sort((a, b) => new Date(b.completed_at || 0) - new Date(a.completed_at || 0));

        return results;
    }

    getScanById(id) {
        return this.data.scan_history.find(s => s.id === id);
    }

    createScan(scanData, certData) {
        const certId = 'cert_' + crypto.randomBytes(4).toString('hex');
        const scanId = 'scan_' + crypto.randomBytes(4).toString('hex');

        const newCert = {
            id: certId,
            user_id: certData.user_id || 'user_001',
            original_filename: certData.original_filename,
            stored_filename: certData.stored_filename,
            file_size: certData.file_size,
            content_type: certData.content_type,
            created_at: new Date().toISOString()
        };

        const now = new Date();
        const dateFormatted = now.toLocaleDateString('en-GB', {
            day: '2-digit',
            month: 'short',
            year: 'numeric'
        }) + ', ' + now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            hour12: true
        });

        const newScan = {
            id: scanId,
            certificate_id: certId,
            user_id: certData.user_id || 'user_001',
            file_name: certData.original_filename,
            date_time_display: dateFormatted,
            analysis_status: 'Completed',
            final_verdict: scanData.final_verdict,
            confidence_score: scanData.confidence_score,
            completed_at: now.toISOString(),
            detailed_ai_results: scanData.detailed_ai_results
        };

        this.data.certificates.unshift(newCert);
        this.data.scan_history.unshift(newScan);
        this.save();

        return newScan;
    }

    deleteScan(id) {
        const index = this.data.scan_history.findIndex(s => s.id === id);
        if (index !== -1) {
            const removed = this.data.scan_history.splice(index, 1)[0];
            this.save();
            return removed;
        }
        return null;
    }
}

module.exports = new Database();
