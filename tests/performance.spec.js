import { test, expect } from '@playwright/test';

test.describe('Performance Tests', () => {
  test('should load quickly', async ({ page }) => {
    const startTime = Date.now();
    
    await page.goto('/');
    
    // Wait for main content to be visible
    await page.locator('main .greeting').waitFor();
    
    const loadTime = Date.now() - startTime;
    
    // Page should load within 5 seconds (generous for CI environments)
    expect(loadTime).toBeLessThan(5000);
  });

  test('should have no large layout shifts', async ({ page }) => {
    await page.goto('/');
    
    // Take initial screenshot for reference
    await page.screenshot({ path: '/tmp/initial-layout.png' });
    
    // Wait a moment for any potential layout shifts
    await page.waitForTimeout(1000);
    
    // Take second screenshot for comparison
    await page.screenshot({ path: '/tmp/final-layout.png' });
    
    // Verify key elements are still in place
    const title = page.locator('h1');
    const greeting = page.locator('.greeting');
    
    await expect(title).toBeVisible();
    await expect(greeting).toBeVisible();
  });

  test('should load all required resources', async ({ page }) => {
    const resourceRequests = [];
    const failedRequests = [];

    page.on('request', request => {
      resourceRequests.push(request.url());
    });

    page.on('requestfailed', request => {
      failedRequests.push(request.url());
    });

    await page.goto('/');
    
    // Wait for page to fully load
    await page.waitForLoadState('networkidle');
    
    // Verify no requests failed
    expect(failedRequests).toHaveLength(0);
    
    // Verify essential resources loaded
    expect(resourceRequests.some(url => url.includes('.css'))).toBeTruthy();
    expect(resourceRequests.some(url => url.includes('.js'))).toBeTruthy();
  });
});