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
                cb(r.sha, null);
            } catch(e) { cb(null, data); }
        });
    });
    req.on('error', (e) => cb(null, e.message));
    req.end();
}

function uploadFile(path, content, sha, cb) {
    const body = JSON.stringify({
        message: 'Update ' + path,
        content: content,
        sha: sha
    });
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
            cb(res.statusCode);
        });
    });
    req.on('error', (e) => { console.error(path + ': ' + e.message); cb(0); });
    req.write(body);
    req.end();
}

const logoContent = fs.readFileSync('c:\\冬\\项目\\文本展示\\logo\\logo_transparent.png').toString('base64');

getSHA('logo.png', (sha, err) => {
    if (sha) {
        uploadFile('logo.png', logoContent, sha, (code) => {
            console.log('Logo updated: ' + code);
        });
    } else {
        console.error('Failed to get SHA: ' + err);
    }
});
