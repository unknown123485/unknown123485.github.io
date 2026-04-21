const https = require('https');
const fs = require('fs');

const token = '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';
const repo = 'unknown123485/unknown123485.github.io';

function getSHA(callback) {
    const options = {
        hostname: 'api.github.com',
        path: '/repos/' + repo + '/contents/index.html',
        method: 'GET',
        headers: { 'User-Agent': 'node.js', 'Authorization': 'token ' + token }
    };
    const req = https.request(options, (res) => {
        let data = '';
        res.on('data', (c) => data += c);
        res.on('end', () => {
            const r = JSON.parse(data);
            callback(r.sha);
        });
    });
    req.on('error', (e) => console.error(e.message));
    req.end();
}

function uploadFile(sha) {
    const content = fs.readFileSync('c:\\冬\\项目\\文本展示\\preview.html', 'utf-8');
    const base64 = Buffer.from(content, 'utf-8').toString('base64');
    
    const body = JSON.stringify({
        message: 'Update v5.3: retro typewriter fix, font sync to matrix, mobile file select fix, immersive status bar, theme carousel, folder memory',
        content: base64,
        sha: sha
    });
    
    const options = {
        hostname: 'api.github.com',
        path: '/repos/' + repo + '/contents/index.html',
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
            console.log('Status: ' + res.statusCode);
            if (res.statusCode === 200) {
                const r = JSON.parse(data);
                console.log('Commit: ' + r.commit.sha);
                console.log('URL: https://unknown123485.github.io/');
            } else {
                console.log(data.substring(0, 500));
            }
        });
    });
    req.on('error', (e) => console.error(e.message));
    req.write(body);
    req.end();
}

getSHA(uploadFile);
