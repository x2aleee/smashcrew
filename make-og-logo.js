const { chromium } = require('playwright');
const fs = require('fs');

const logoPath = fs.realpathSync('SMASH LOGO.svg').replace(/\\/g, '/');
const src = 'file:///' + logoPath;

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewportSize: { width: 1200, height: 630 } });

  await page.setContent(
    '<!doctype html><html><head><meta charset="utf-8"><style>' +
    'html,body{margin:0;padding:0;background:#000000;height:100%;}' +
    '.wrap{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;}' +
    'img{display:block;max-width:1130px;max-height:560px;height:auto;width:auto;object-fit:contain;}' +
    '</style></head><body><div class="wrap"><img src="' + src + '" alt="Smash Crew"></div></body></html>',
    { waitUntil: 'domcontentloaded' }
  );

  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'assets/og-logo.png', fullPage: false });
  await browser.close();

  const stat = fs.statSync('assets/og-logo.png');
  console.log('created assets/og-logo.png', stat.size, 'bytes');
})().catch(e => { console.error(e); process.exit(1); });
