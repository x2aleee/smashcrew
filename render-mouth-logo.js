const { chromium } = require('playwright');
const fs = require('fs');

const logoFile = 'assets/logo.svg';
const svgPath = fs.realpathSync(logoFile).replace(/\\/g, '/');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewportSize: { width: 480, height: 480 } });
  await page.setContent(
    '<!doctype html><html><head><meta charset="utf-8"><style>' +
    'html,body{margin:0;padding:0;background:#ffffff;}' +
    'img{display:block;max-width:480px;max-height:480px;height:auto;width:auto;}' +
    '</style></head><body><img src="file:///' + svgPath + '"></body></html>',
    { waitUntil: 'domcontentloaded' }
  );
  await page.waitForTimeout(2500);
  await page.screenshot({ path: 'assets/og-mouth-logo-source.png', fullPage: false });
  await browser.close();
  console.log('source', fs.statSync('assets/og-mouth-logo-source.png').size, 'bytes');
})().catch(e => { console.error(e); process.exit(1); });
