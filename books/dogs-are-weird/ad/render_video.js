// Renders ad/video.html to frames (30 fps, 15 s) for ffmpeg.
const { chromium } = require('playwright'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1920, height: 1080 } });
  await p.goto('file://' + path.join(__dirname, 'video.html'));
  await p.evaluate(() => document.fonts.ready);
  await p.waitForTimeout(500);
  const only = process.argv[2] ? process.argv[2].split(',').map(Number) : null;
  const N = 450;
  for (let i = 0; i < N; i++) {
    if (only && !only.includes(i)) continue;
    await p.evaluate(t => setT(t), i / 30);
    await p.screenshot({ path: path.join(__dirname, 'frames', String(i).padStart(4, '0') + '.jpg'), type: 'jpeg', quality: 92 });
  }
  await b.close();
})();
