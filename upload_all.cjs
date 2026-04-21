const https = require('https');
const fs = require('fs');
const path = require('path');

const token = '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';
const repo = 'unknown123485/unknown123485.github.io';

function githubRequest(method, apiPath, body) {
    return new Promise((resolve, reject) => {
        const options = {
            hostname: 'api.github.com',
            path: apiPath,
            method: method,
            headers: {
                'User-Agent': 'node.js',
                'Authorization': 'token ' + token,
                'Content-Type': 'application/json'
            }
        };
        const req = https.request(options, (res) => {
            let data = '';
            res.on('data', (c) => data += c);
            res.on('end', () => {
                try {
                    const parsed = JSON.parse(data);
                    resolve({ status: res.statusCode, data: parsed });
                } catch (e) {
                    resolve({ status: res.statusCode, data: data });
                }
            });
        });
        req.on('error', reject);
        if (body) req.write(body);
        req.end();
    });
}

function getFileSHA(repoPath) {
    return githubRequest('GET', '/repos/' + repo + '/contents/' + repoPath)
        .then(r => r.status === 200 ? r.data.sha : null)
        .catch(() => null);
}

function uploadFile(localPath, repoPath, message, sha) {
    const content = fs.readFileSync(localPath);
    const base64 = content.toString('base64');
    
    const bodyObj = {
        message: message,
        content: base64
    };
    if (sha) bodyObj.sha = sha;
    
    const body = JSON.stringify(bodyObj);
    
    return githubRequest('PUT', '/repos/' + repo + '/contents/' + repoPath, body);
}

async function main() {
    const files = [
        {
            local: 'c:\\冬\\项目\\文本展示\\preview.html',
            repo: 'index.html',
            msg: 'v6.0beta: ABOUT pill shape, theme carousel refactor, scroll throttle, lazy init, splash screen, lifecycle management'
        },
        {
            local: 'c:\\冬\\项目\\文本展示\\fonts\\hyzhengyuan\\HYZhengYuan-subset.woff2',
            repo: 'assets/fonts/hyzhengyuan/HYZhengYuan-subset.woff2',
            msg: 'Update HYZhengYuan subset font (woff2)'
        },
        {
            local: 'c:\\冬\\项目\\文本展示\\fonts\\hyzhengyuan\\result.css',
            repo: 'assets/fonts/hyzhengyuan/result.css',
            msg: 'Update HYZhengYuan font CSS'
        },
        {
            local: 'c:\\冬\\项目\\文本展示\\fonts\\jinghuaoldsong\\JingHuaOldSong-subset.woff2',
            repo: 'assets/fonts/jinghuaoldsong/JingHuaOldSong-subset.woff2',
            msg: 'Update JingHuaOldSong subset font (woff2)'
        },
        {
            local: 'c:\\冬\\项目\\文本展示\\fonts\\jinghuaoldsong\\result.css',
            repo: 'assets/fonts/jinghuaoldsong/result.css',
            msg: 'Update JingHuaOldSong font CSS'
        },
        {
            local: 'c:\\冬\\项目\\文本展示\\fonts\\huiwenmingchao\\HuiWenMingChao-subset.woff2',
            repo: 'assets/fonts/huiwenmingchao/HuiWenMingChao-subset.woff2',
            msg: 'Update HuiWenMingChao subset font (woff2)'
        },
        {
            local: 'c:\\冬\\项目\\文本展示\\fonts\\huiwenmingchao\\result.css',
            repo: 'assets/fonts/huiwenmingchao/result.css',
            msg: 'Update HuiWenMingChao font CSS'
        }
    ];

    for (const file of files) {
        console.log('Uploading ' + file.repo + '...');
        try {
            const sha = await getFileSHA(file.repo);
            const result = await uploadFile(file.local, file.repo, file.msg, sha);
            if (result.status === 200 || result.status === 201) {
                console.log('  OK: ' + result.data.commit.sha);
            } else {
                console.log('  Error ' + result.status + ': ' + JSON.stringify(result.data).substring(0, 200));
            }
        } catch (e) {
            console.log('  Failed: ' + e.message);
        }
    }
    console.log('All uploads complete.');
    console.log('URL: https://unknown123485.github.io/');
}

main();
