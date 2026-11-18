// Rasterize art/svg/*.svg -> images/*.png with Chromium. Usage: node art/render_svgs.js [filter]
const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const src = path.join(__dirname, 'svg'), dst = path.join(__dirname, '..', 'images');
  fs.mkdirSync(dst, { recursive: true });
  const filt = process.argv[2] || '';
  const files = fs.readdirSync(src).filter(f => f.endsWith('.svg') && f.includes(filt));
  const b = await chromium.launch(); const p = await b.newPage({ deviceScaleFactor: 1.6 });
  for (const f of files) {
    const svg = fs.readFileSync(path.join(src, f), 'utf8');
    const m = svg.match(/viewBox="0 0 (\d+) (\d+)"/); const W = +m[1], H = +m[2];
    const scale = Math.min(2, 3000 / Math.max(W, H)) * 1.0;
    await p.setViewportSize({ width: W, height: H });
    await p.setContent(`<html><body style="margin:0">${svg.replace(/width="\d+" height="\d+"/, `width="${W}" height="${H}"`)}</body></html>`);
    const out = path.join(dst, f.replace('.svg', '.jpg'));
    await p.screenshot({ path: out, clip: { x: 0, y: 0, width: W, height: H }, type: 'jpeg', quality: 90 });
  }
  await b.close(); console.log('rendered', files.length);
})();
