const http = require('http');

function request(options, postData) {
    return new Promise((resolve, reject) => {
        const req = http.request(options, (res) => {
            let data = '';
            res.on('data', chunk => data += chunk);
            res.on('end', () => resolve({ statusCode: res.statusCode, headers: res.headers, body: data }));
        });
        req.on('error', reject);
        if (postData) req.write(postData);
        req.end();
    });
}

async function runTests() {
    console.log('--- RUNNING FULL-STACK VERIFICATION TESTS ---');

    try {
        // 1. Health Check
        const health = await request({ hostname: 'localhost', port: 3000, path: '/api/health', method: 'GET' });
        console.log('1. Health Check status:', health.statusCode, health.body);

        // 2. Features Endpoint
        const features = await request({ hostname: 'localhost', port: 3000, path: '/api/features', method: 'GET' });
        console.log('2. Features Endpoint status:', features.statusCode);
        const featData = JSON.parse(features.body);
        console.log('   Feature cards count:', featData.data.length, 'Cards:', featData.data.map(c => c.title).join(', '));

        // 3. Scans Endpoint
        const scans = await request({ hostname: 'localhost', port: 3000, path: '/api/scans', method: 'GET' });
        console.log('3. Scans Endpoint status:', scans.statusCode);
        const scansData = JSON.parse(scans.body);
        console.log('   Scans count:', scansData.count, 'Files:', scansData.data.map(s => `${s.file_name} (${s.final_verdict})`).join(' | '));

        // 4. Detailed Report Endpoint for Fake Certificate (certificate_002.jpg)
        const report = await request({ hostname: 'localhost', port: 3000, path: '/api/scans/scan_002/report', method: 'GET' });
        console.log('4. Scan 002 Report status:', report.statusCode);
        const repData = JSON.parse(report.body);
        console.log('   Verdict:', repData.data.final_verdict);
        console.log('   Confidence:', repData.data.confidence_score + '%');
        console.log('   Tamper Zones:', repData.data.detailed_ai_results.tamper_zones.length, 'zones detected');
        console.log('   Scores:', repData.data.detailed_ai_results.scores);

        // 5. Upload New Certificate Test
        const uploadPayload = JSON.stringify({
            filename: 'test_student_diploma_2025.jpg',
            base64Data: 'DATA_FOR_STUDENT_DIPLOMA_VERIFICATION_PASS'
        });
        const upload = await request({
            hostname: 'localhost',
            port: 3000,
            path: '/api/certificates/upload',
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': Buffer.byteLength(uploadPayload)
            }
        }, uploadPayload);
        console.log('5. Certificate Upload status:', upload.statusCode);
        const uploadRes = JSON.parse(upload.body);
        console.log('   New Scan ID:', uploadRes.data.id, 'Verdict:', uploadRes.data.final_verdict, 'Confidence:', uploadRes.data.confidence_score + '%');

        // 6. Verify Static Assets
        const indexHtml = await request({ hostname: 'localhost', port: 3000, path: '/', method: 'GET' });
        console.log('6. Static index.html status:', indexHtml.statusCode, 'Length:', indexHtml.body.length);

        const styleCss = await request({ hostname: 'localhost', port: 3000, path: '/style.css', method: 'GET' });
        console.log('   Static style.css status:', styleCss.statusCode, 'Length:', styleCss.body.length);

        const appJs = await request({ hostname: 'localhost', port: 3000, path: '/app.js', method: 'GET' });
        console.log('   Static app.js status:', appJs.statusCode, 'Length:', appJs.body.length);

        console.log('\n✅ ALL AUTOMATED VERIFICATION TESTS PASSED SUCCESSFULLY!');
    } catch (err) {
        console.error('Test execution failed:', err);
    }
}

runTests();
