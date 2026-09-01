const http = require('http');
const fs = require('fs');
const path = require('path');
const url = require('url');
const crypto = require('crypto');
const db = require('./database');
const aiEngine = require('./ai_engine');
const auth = require('./auth');

const PORT = process.env.PORT || 3000;
const PUBLIC_DIR = path.join(__dirname, '..', 'public');
const UPLOADS_DIR = path.join(__dirname, '..', 'public', 'uploads');

// Ensure directories exist
if (!fs.existsSync(PUBLIC_DIR)) fs.mkdirSync(PUBLIC_DIR, { recursive: true });
if (!fs.existsSync(UPLOADS_DIR)) fs.mkdirSync(UPLOADS_DIR, { recursive: true });

// MIME types for static serving
const MIME_TYPES = {
    '.html': 'text/html; charset=utf-8',
    '.css': 'text/css; charset=utf-8',
    '.js': 'application/javascript; charset=utf-8',
    '.json': 'application/json; charset=utf-8',
    '.png': 'image/png',
    '.jpg': 'image/jpeg',
    '.jpeg': 'image/jpeg',
    '.svg': 'image/svg+xml',
    '.webp': 'image/webp',
    '.ico': 'image/x-icon',
    '.pdf': 'application/pdf'
};

// Simple Multipart / Body Parser Helper
function parseRequestBody(req) {
    return new Promise((resolve, reject) => {
        const contentType = req.headers['content-type'] || '';
        const chunks = [];

        req.on('data', chunk => chunks.push(chunk));
        req.on('end', () => {
            const buffer = Buffer.concat(chunks);

            if (contentType.includes('application/json')) {
                try {
                    const json = JSON.parse(buffer.toString('utf8'));
                    resolve({ type: 'json', data: json });
                } catch (e) {
                    resolve({ type: 'json', data: {} });
                }
            } else if (contentType.includes('multipart/form-data')) {
                // Parse multipart boundary
                const match = contentType.match(/boundary=(?:"([^"]+)"|([^;]+))/i);
                if (!match) {
                    resolve({ type: 'raw', buffer });
                    return;
                }
                const boundary = match[1] || match[2];
                const parts = parseMultipart(buffer, boundary);
                resolve({ type: 'multipart', parts });
            } else {
                resolve({ type: 'raw', buffer, text: buffer.toString('utf8') });
            }
        });
        req.on('error', reject);
    });
}

// Multipart parser for files and fields
function parseMultipart(buffer, boundary) {
    const boundaryBuffer = Buffer.from('--' + boundary);
    const parts = [];
    let start = 0;

    while (start < buffer.length) {
        const boundaryIdx = buffer.indexOf(boundaryBuffer, start);
        if (boundaryIdx === -1) break;

        const nextBoundaryIdx = buffer.indexOf(boundaryBuffer, boundaryIdx + boundaryBuffer.length);
        if (nextBoundaryIdx === -1) break;

        const partBuffer = buffer.slice(boundaryIdx + boundaryBuffer.length, nextBoundaryIdx);
        const headerEndIdx = partBuffer.indexOf(Buffer.from('\r\n\r\n'));

        if (headerEndIdx !== -1) {
            const headerStr = partBuffer.slice(0, headerEndIdx).toString('utf8');
            let dataBuffer = partBuffer.slice(headerEndIdx + 4);

            // Strip trailing \r\n
            if (dataBuffer.length >= 2 && dataBuffer[dataBuffer.length - 2] === 0x0D && dataBuffer[dataBuffer.length - 1] === 0x0A) {
                dataBuffer = dataBuffer.slice(0, dataBuffer.length - 2);
            }

            const nameMatch = headerStr.match(/name="([^"]+)"/);
            const filenameMatch = headerStr.match(/filename="([^"]+)"/);
            const contentTypeMatch = headerStr.match(/Content-Type:\s*([^\r\n]+)/i);

            if (filenameMatch) {
                parts.push({
                    name: nameMatch ? nameMatch[1] : 'file',
                    filename: filenameMatch[1],
                    contentType: contentTypeMatch ? contentTypeMatch[1].trim() : 'application/octet-stream',
                    data: dataBuffer
                });
            } else if (nameMatch) {
                parts.push({
                    name: nameMatch[1],
                    value: dataBuffer.toString('utf8')
                });
            }
        }

        start = nextBoundaryIdx;
    }

    return parts;
}

// Helper to send JSON responses
function sendJSON(res, statusCode, data) {
    res.writeHead(statusCode, {
        'Content-Type': 'application/json; charset=utf-8',
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type, Authorization',
        'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
    });
    res.end(JSON.stringify(data));
}

// Server request handler
const server = http.createServer(async (req, res) => {
    const parsedUrl = url.parse(req.url, true);
    const pathname = parsedUrl.pathname;
    const method = req.method.toUpperCase();

    // CORS preflight
    if (method === 'OPTIONS') {
        res.writeHead(204, {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Headers': 'Content-Type, Authorization',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
        });
        res.end();
        return;
    }

    try {
        // --- API ROUTES ---

        // 1. Health Check
        if (pathname === '/api/health') {
            return sendJSON(res, 200, { status: 'healthy', timestamp: new Date().toISOString() });
        }

        // 2. Auth Endpoints
        if (pathname === '/api/auth/login' && method === 'POST') {
            const body = await parseRequestBody(req);
            const { email, password } = body.data || {};
            
            const user = db.findUserByEmail(email || '');
            if (!user) {
                return sendJSON(res, 401, { success: false, message: 'Invalid credentials. Use demo@sunbreathing.ai / password123' });
            }

            const inputHash = crypto.createHash('sha256').update(password || '').digest('hex');
            if (user.passwordHash !== inputHash) {
                return sendJSON(res, 401, { success: false, message: 'Invalid email or password.' });
            }

            const token = auth.generateToken(user);
            return sendJSON(res, 200, {
                success: true,
                token,
                user: { id: user.id, name: user.name, email: user.email, role: user.role, organization: user.organization }
            });
        }

        if (pathname === '/api/auth/register' && method === 'POST') {
            const body = await parseRequestBody(req);
            const { name, email, password, organization } = body.data || {};

            if (!email || !password) {
                return sendJSON(res, 400, { success: false, message: 'Email and password are required.' });
            }

            if (db.findUserByEmail(email)) {
                return sendJSON(res, 400, { success: false, message: 'Email already registered.' });
            }

            const passwordHash = crypto.createHash('sha256').update(password).digest('hex');
            const newUser = db.createUser({
                name: name || 'Verifier',
                email,
                passwordHash,
                organization: organization || 'Academic Institute',
                role: 'Inspector'
            });

            const token = auth.generateToken(newUser);
            return sendJSON(res, 201, {
                success: true,
                token,
                user: { id: newUser.id, name: newUser.name, email: newUser.email, role: newUser.role, organization: newUser.organization }
            });
        }

        if (pathname === '/api/auth/me' && method === 'GET') {
            const user = auth.getUserFromReq(req);
            if (!user) {
                return sendJSON(res, 401, { success: false, message: 'Unauthorized' });
            }
            return sendJSON(res, 200, {
                success: true,
                user: { id: user.id, name: user.name, email: user.email, role: user.role, organization: user.organization }
            });
        }

        if (pathname === '/api/auth/logout' && method === 'POST') {
            return sendJSON(res, 200, { success: true, message: 'Logged out successfully.' });
        }

        // 3. Dynamic Feature Cards
        if (pathname === '/api/features' && method === 'GET') {
            const features = db.getFeatureCards();
            return sendJSON(res, 200, { success: true, data: features });
        }

        if (pathname.startsWith('/api/features/') && method === 'PUT') {
            const cardId = pathname.replace('/api/features/', '');
            const body = await parseRequestBody(req);
            const updated = db.updateFeatureCard(cardId, body.data || {});
            if (!updated) {
                return sendJSON(res, 404, { success: false, message: 'Feature card not found.' });
            }
            return sendJSON(res, 200, { success: true, data: updated });
        }

        // 4. Scan History & Filtering
        if (pathname === '/api/scans' && method === 'GET') {
            const { verdict, search, sort } = parsedUrl.query;
            const scans = db.getScans({ verdict, search, sort });
            return sendJSON(res, 200, {
                success: true,
                count: scans.length,
                data: scans
            });
        }

        // 5. Detailed Scan Report
        if (pathname.match(/^\/api\/scans\/[^/]+\/report$/) && method === 'GET') {
            const scanId = pathname.split('/')[3];
            const scan = db.getScanById(scanId);
            if (!scan) {
                return sendJSON(res, 404, { success: false, message: 'Scan report not found.' });
            }
            return sendJSON(res, 200, { success: true, data: scan });
        }

        // 6. Delete Scan
        if (pathname.startsWith('/api/scans/') && method === 'DELETE') {
            const scanId = pathname.replace('/api/scans/', '');
            const removed = db.deleteScan(scanId);
            if (!removed) {
                return sendJSON(res, 404, { success: false, message: 'Scan not found.' });
            }
            return sendJSON(res, 200, { success: true, message: 'Scan deleted successfully.' });
        }

        // 7. Certificate Upload & AI Analysis
        if (pathname === '/api/certificates/upload' && method === 'POST') {
            const user = auth.getUserFromReq(req);
            const body = await parseRequestBody(req);

            let fileBuffer = null;
            let originalFilename = 'certificate_upload.jpg';
            let contentType = 'image/jpeg';

            if (body.type === 'multipart' && body.parts) {
                const filePart = body.parts.find(p => p.filename);
                if (filePart) {
                    fileBuffer = filePart.data;
                    originalFilename = filePart.filename;
                    contentType = filePart.contentType;
                }
            } else if (body.type === 'json' && body.data) {
                // Support base64 upload or preset sample selection
                const { base64Data, filename, sampleId } = body.data;
                if (base64Data) {
                    const matches = base64Data.match(/^data:([A-Za-z-+\/]+);base64,(.+)$/);
                    if (matches) {
                        contentType = matches[1];
                        fileBuffer = Buffer.from(matches[2], 'base64');
                    } else {
                        fileBuffer = Buffer.from(base64Data, 'base64');
                    }
                    originalFilename = filename || 'certificate.jpg';
                } else if (sampleId) {
                    // Handle pre-baked sample
                    const sampleCert = db.getScanById(sampleId);
                    if (sampleCert) {
                        return sendJSON(res, 200, {
                            success: true,
                            data: sampleCert
                        });
                    }
                }
            }

            if (!fileBuffer || fileBuffer.length === 0) {
                // Fallback default mock buffer if empty
                fileBuffer = Buffer.from('MOCK_CERTIFICATE_DATA_' + Date.now());
            }

            // Max file size 5MB check
            if (fileBuffer.length > 5 * 1024 * 1024) {
                return sendJSON(res, 400, { success: false, message: 'File exceeds maximum 5MB size limit.' });
            }

            // Save file securely to uploads directory
            const fileExt = path.extname(originalFilename) || '.jpg';
            const storedFilename = `cert_${Date.now()}_${crypto.randomBytes(4).toString('hex')}${fileExt}`;
            const storedPath = path.join(UPLOADS_DIR, storedFilename);
            fs.writeFileSync(storedPath, fileBuffer);

            // Execute AI manipulation forensics
            const analysisResult = await aiEngine.analyzeCertificate(fileBuffer, originalFilename, contentType);

            // Store in database
            const createdScan = db.createScan({
                final_verdict: analysisResult.verdict,
                confidence_score: analysisResult.confidence,
                detailed_ai_results: analysisResult
            }, {
                user_id: user ? user.id : 'user_001',
                original_filename: originalFilename,
                stored_filename: storedFilename,
                file_size: fileBuffer.length,
                content_type: contentType
            });

            return sendJSON(res, 201, {
                success: true,
                message: 'Certificate analyzed successfully.',
                data: createdScan
            });
        }

        // --- STATIC FILE SERVING ---
        let filePath = path.join(PUBLIC_DIR, pathname === '/' ? 'index.html' : pathname);

        // Security check: prevent directory traversal
        if (!filePath.startsWith(PUBLIC_DIR)) {
            res.writeHead(403, { 'Content-Type': 'text/plain' });
            res.end('Forbidden');
            return;
        }

        // If file exists, serve it
        if (fs.existsSync(filePath) && fs.statSync(filePath).isFile()) {
            const ext = path.extname(filePath).toLowerCase();
            const mimeType = MIME_TYPES[ext] || 'application/octet-stream';

            res.writeHead(200, {
                'Content-Type': mimeType,
                'Cache-Control': 'no-cache'
            });
            fs.createReadStream(filePath).pipe(res);
            return;
        }

        // Fallback to index.html for SPA routes
        const indexPath = path.join(PUBLIC_DIR, 'index.html');
        if (fs.existsSync(indexPath)) {
            res.writeHead(200, { 'Content-Type': 'text/html; charset=utf-8' });
            fs.createReadStream(indexPath).pipe(res);
            return;
        }

        res.writeHead(404, { 'Content-Type': 'text/plain' });
        res.end('Not Found');

    } catch (err) {
        console.error('Server error:', err);
        sendJSON(res, 500, { success: false, message: 'Internal Server Error', error: err.message });
    }
});

server.listen(PORT, () => {
    console.log(`=================================================`);
    console.log(`🚀 Fake Certificate Detection Server Running!`);
    console.log(`🌐 Dashboard URL: http://localhost:${PORT}`);
    console.log(`📡 REST API Base: http://localhost:${PORT}/api`);
    console.log(`=================================================`);
});
