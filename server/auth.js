const crypto = require('crypto');
const db = require('./database');

const JWT_SECRET = 'sun-breathing-ai-secret-key-2025-cert-verif-secure';

class Auth {
    // Generate simple HMAC token
    generateToken(user) {
        const payload = {
            id: user.id,
            email: user.email,
            name: user.name,
            role: user.role || 'User',
            iat: Math.floor(Date.now() / 1000),
            exp: Math.floor(Date.now() / 1000) + (7 * 24 * 60 * 60) // 7 days
        };
        const header = { alg: 'HS256', typ: 'JWT' };

        const b64Header = Buffer.from(JSON.stringify(header)).toString('base64url');
        const b64Payload = Buffer.from(JSON.stringify(payload)).toString('base64url');
        const signature = crypto
            .createHmac('sha256', JWT_SECRET)
            .update(`${b64Header}.${b64Payload}`)
            .digest('base64url');

        return `${b64Header}.${b64Payload}.${signature}`;
    }

    verifyToken(token) {
        if (!token) return null;
        try {
            const parts = token.split('.');
            if (parts.length !== 3) return null;

            const [b64Header, b64Payload, signature] = parts;
            const expectedSig = crypto
                .createHmac('sha256', JWT_SECRET)
                .update(`${b64Header}.${b64Payload}`)
                .digest('base64url');

            if (signature !== expectedSig) return null;

            const payload = JSON.parse(Buffer.from(b64Payload, 'base64url').toString('utf8'));
            if (payload.exp && payload.exp < Math.floor(Date.now() / 1000)) {
                return null; // Expired
            }
            return payload;
        } catch (err) {
            return null;
        }
    }

    // Extract user from request headers
    getUserFromReq(req) {
        const authHeader = req.headers['authorization'] || '';
        let token = null;

        if (authHeader.startsWith('Bearer ')) {
            token = authHeader.substring(7);
        } else if (req.headers['cookie']) {
            const match = req.headers['cookie'].match(/auth_token=([^;]+)/);
            if (match) token = match[1];
        }

        if (!token) {
            // Default to demo user for seamless UX if no token is provided
            return db.findUserById('user_001');
        }

        const payload = this.verifyToken(token);
        if (payload) {
            return db.findUserById(payload.id) || payload;
        }
        return db.findUserById('user_001');
    }
}

module.exports = new Auth();
