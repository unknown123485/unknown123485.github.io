const fs = require('fs');
const zlib = require('zlib');

const inputPath = 'c:\\冬\\项目\\文本展示\\logo\\logo.png';
const outputPath = 'c:\\冬\\项目\\文本展示\\logo\\logo_transparent.png';

const buf = fs.readFileSync(inputPath);

function readU32BE(b, off) { return (b[off]<<24)|(b[off+1]<<16)|(b[off+2]<<8)|b[off+3]; }
function writeU32BE(v) { const b = Buffer.alloc(4); b.writeUInt32BE(v); return b; }
function writeU32LE(v) { const b = Buffer.alloc(4); b.writeUInt32LE(v); return b; }

if (buf[0]!==0x89||buf[1]!==0x50) { console.error('Not PNG'); process.exit(1); }

let chunks = [];
let offset = 8;
while (offset < buf.length) {
    const len = readU32BE(buf, offset);
    const type = buf.slice(offset+4, offset+8).toString('ascii');
    const data = buf.slice(offset+8, offset+8+len);
    chunks.push({ len, type, data });
    offset += 12 + len;
}

const ihdr = chunks.find(c => c.type === 'IHDR');
const width = readU32BE(ihdr.data, 0);
const height = readU32BE(ihdr.data, 4);
const bitDepth = ihdr.data[8];
const colorType = ihdr.data[9];
console.log('Size: ' + width + 'x' + height + ' bitDepth=' + bitDepth + ' colorType=' + colorType);

const idatData = Buffer.concat(chunks.filter(c => c.type === 'IDAT').map(c => c.data));
const raw = zlib.inflateSync(idatData);

const bpp = colorType === 6 ? 4 : (colorType === 2 ? 3 : (colorType === 4 ? 2 : 1));
const stride = 1 + width * bpp;
const threshold = 235;

for (let y = 0; y < height; y++) {
    const rowOff = y * stride;
    for (let x = 0; x < width; x++) {
        const px = rowOff + 1 + x * bpp;
        const r = raw[px];
        const g = raw[px + 1];
        const b = raw[px + 2];
        if (r >= threshold && g >= threshold && b >= threshold) {
            const avg = (r + g + b) / 3;
            if (colorType === 6) {
                const a = raw[px + 3];
                const factor = Math.max(0, (255 - avg) / (255 - threshold));
                raw[px + 3] = Math.round(a * factor);
            }
        }
    }
}

const newIdat = zlib.deflateSync(raw, { level: 9 });

function crc32(buf) {
    let c = 0xFFFFFFFF;
    for (let i = 0; i < buf.length; i++) {
        c ^= buf[i];
        for (let j = 0; j < 8; j++) c = (c >>> 1) ^ (c & 1 ? 0xEDB88320 : 0);
    }
    return (c ^ 0xFFFFFFFF) >>> 0;
}

function makeChunk(type, data) {
    const t = Buffer.from(type, 'ascii');
    const l = writeU32BE(data.length);
    const crcBuf = Buffer.alloc(4);
    crcBuf.writeUInt32BE(crc32(Buffer.concat([t, data])));
    return Buffer.concat([l, t, data, crcBuf]);
}

const sig = Buffer.from([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A]);
const ihdrChunk = makeChunk('IHDR', ihdr.data);
const idatChunk = makeChunk('IDAT', newIdat);
const iendChunk = makeChunk('IEND', Buffer.alloc(0));

const out = Buffer.concat([sig, ihdrChunk, idatChunk, iendChunk]);
fs.writeFileSync(outputPath, out);
console.log('Saved: ' + outputPath + ' (' + out.length + ' bytes)');
