const https = require('https');
const fs = require('fs');

const token = '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';
const repo = 'unknown123485/unknown123485.github.io';

function getSHA(path, cb) {
    const options = {
        hostname: 'api.github.com',
        path: '/repos/' + repo + '/contents/' + path,
        method: 'GET',
        headers: { 'User-Agent': 'node.js', 'Authorization': 'token ' + token }
    };
    const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (c) => data += c);
        res.on('end', () => {
            try {
                const r = JSON.parse(data);
                if (r.sha) cb(r.sha, null);
                else cb(null, r.message || 'no sha');
            } catch(e) { cb(null, data); }
        });
    });
    req.on('error', (e) => cb(null, e.message));
    req.end();
}

function uploadFile(path, content, sha, cb) {
    const payload = { message: 'Update ' + path, content: content };
    if (sha) payload.sha = sha;
    const body = JSON.stringify(payload);
    const options = {
        hostname: 'api.github.com',
        path: '/repos/' + repo + '/contents/' + path,
        method: 'PUT',
        headers: {
            'User-Agent': 'node.js',
            'Authorization': 'token ' + token,
            'Content-Type': 'application/json',
            'Content-Length': Buffer.byteLength(body)
        }
    };
    const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (c) => data += c);
        res.on('end', () => {
            console.log(path + ': HTTP ' + res.statusCode);
            if (res.statusCode >= 400) console.log('Response: ' + data.substring(0, 300));
            cb(res.statusCode);
        });
    });
    req.on('timeout', () => { console.error(path + ': request timeout'); req.destroy(); cb(0); });
    req.on('error', (e) => { console.error(path + ': ' + e.message); cb(0); });
    req.setTimeout(60000);
    req.write(body);
    req.end();
}

const files = [
    { remote: 'index.html', local: 'c:\\冬\\项目\\文本展示\\preview.html' },
    { remote: 'logo/logo.png', local: 'c:\\冬\\项目\\文本展示\\logo\\logo.png' }
];

let completed = 0;
files.forEach(file => {
    const content = fs.readFileSync(file.local).toString('base64');
    getSHA(file.remote, (sha, err) => {
        if (sha) {
            uploadFile(file.remote, content, sha, (code) => {
                console.log(file.remote + ' updated: ' + code);
                completed++;
                if (completed === files.length) console.log('All files uploaded!');
            });
        } else {
            console.log(file.remote + ' SHA error: ' + err + ', creating new...');
            uploadFile(file.remote, content, null, (code) => {
                console.log(file.remote + ' created: ' + code);
                completed++;
                if (completed === files.length) console.log('All files uploaded!');
            });
        }
    });
});
