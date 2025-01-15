const { chromium } = require('playwright');  // Import Playwright's Chromium module

(async () => {
    // Launch a new browser instance in headless mode (no UI)
    const browser = await chromium.launch({ headless: true });

    // Open a new page/tab in the browser
    const page = await browser.newPage();

    // Navigate to a website
    await page.goto('https://example.com');

    // Extract the title of the page
    const title = await page.title();
    console.log('Page Title:', title);

    // Close the browser
    await browser.close();
})();
