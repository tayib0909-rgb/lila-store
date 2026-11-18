// Renders build/interior.html -> output/interior.pdf (and cover) with Chromium.
// Usage: node build/render.js [interior|cover|all] [--png pageNumbers]
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const which = process.argv[2] || 'all';
  const pngArg = process.argv.indexOf('--png');
  const pngPages = pngArg > 0 ? process.argv[pngArg + 1].split(',').map(Number) : [];
  const out = path.join(__dirname, '..', 'output'); fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const jobs = [];
  if (which === 'all' || which === 'interior') jobs.push(['interior.html', 'interior.pdf']);
  if (which === 'all' || which === 'cover') jobs.push(['cover.html', 'cover.pdf']);
  for (const [src, dst] of jobs) {
    const page = await browser.newPage();
    await page.goto('file://' + path.join(__dirname, src), { waitUntil: 'load' });
    await page.evaluate(() => document.fonts.ready);
    await page.waitForFunction(() => window.__fitDone === true || !document.querySelector('.fitbox'), null, { timeout: 120000 });
    const rep = await page.evaluate(() => window.__fitReport || []);
    const over = rep.filter(r => r.status === 'OVERFLOW');
    console.log(src, 'shrunk:', rep.filter(r => r.status === 'shrunk').length, 'overflow:', over.map(r => r.page).join(',') || 'none');
    await page.pdf({ path: path.join(out, dst), preferCSSPageSize: true, printBackground: true });
    for (const n of pngPages) {
      if (src !== 'interior.html') continue;
      const el = await page.$(`.page[data-p="${n}"]`);
      if (el) await el.screenshot({ path: path.join(out, `preview-p${String(n).padStart(3,'0')}.png`) });
    }
    console.log('wrote', dst);
  }
  await browser.close();
})();
