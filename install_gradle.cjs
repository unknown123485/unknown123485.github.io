const fs = require('fs');
const path = require('path');
const { execSync } = require('child_process');

const homeDir = process.env.USERPROFILE || process.env.HOME;
const gradleCacheDir = path.join(homeDir, '.gradle', 'wrapper', 'dists', 'gradle-8.11.1-all');
const srcZip = path.join(process.env.TEMP || 'C:\\Windows\\Temp', 'gradle-8.11.1-all.zip');

if (!fs.existsSync(gradleCacheDir)) {
    fs.mkdirSync(gradleCacheDir, { recursive: true });
}

const hashDirs = fs.readdirSync(gradleCacheDir).filter(d => {
    return fs.statSync(path.join(gradleCacheDir, d)).isDirectory();
});

let targetDir;
if (hashDirs.length > 0) {
    targetDir = path.join(gradleCacheDir, hashDirs[0]);
} else {
    targetDir = path.join(gradleCacheDir, 'custom_hash');
    fs.mkdirSync(targetDir, { recursive: true });
}

const destZip = path.join(targetDir, 'gradle-8.11.1-all.zip');
if (!fs.existsSync(destZip)) {
    console.log('Copying gradle zip to cache:', destZip);
    fs.copyFileSync(srcZip, destZip);
} else {
    console.log('Gradle zip already exists in cache');
}

const okFile = path.join(targetDir, 'gradle-8.11.1-all.zip.ok');
if (!fs.existsSync(okFile)) {
    fs.writeFileSync(okFile, '');
    console.log('Created .ok marker file');
}

const extractDir = path.join(targetDir, 'gradle-8.11.1');
if (!fs.existsSync(extractDir)) {
    console.log('Extracting gradle...');
    try {
        execSync(`powershell -Command "Expand-Archive -Path '${destZip}' -DestinationPath '${targetDir}' -Force"`, { timeout: 120000 });
        console.log('Extraction complete');
    } catch(e) {
        console.log('Extraction error:', e.message);
    }
} else {
    console.log('Gradle already extracted');
}

console.log('Done. Cache dir:', targetDir);
console.log('Contents:', fs.readdirSync(targetDir));
