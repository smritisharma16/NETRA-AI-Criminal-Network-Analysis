import puppeteer from 'puppeteer';

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  page.on('console', msg => console.log('BROWSER CONSOLE:', msg.text()));
  page.on('pageerror', error => console.log('BROWSER ERROR:', error.message));
  page.on('requestfailed', request => console.log('REQUEST FAILED:', request.url(), request.failure().errorText));
  
  console.log("Navigating to http://localhost:5173/dashboard...");
  try {
      await page.goto('http://localhost:5173/dashboard', { waitUntil: 'networkidle0', timeout: 10000 });
  } catch (e) {
      console.log("Navigation issue:", e.message);
  }
  
  await new Promise(r => setTimeout(r, 2000));
  await browser.close();
})();
