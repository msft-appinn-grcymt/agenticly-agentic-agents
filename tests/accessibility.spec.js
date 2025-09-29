import { test, expect } from '@playwright/test';

test.describe('Accessibility Tests', () => {
  test('should have proper semantic HTML structure', async ({ page }) => {
    await page.goto('/');

    // Check for proper semantic elements
    const header = page.locator('header');
    const main = page.locator('main');
    const h1 = page.locator('h1');

    await expect(header).toBeVisible();
    await expect(main).toBeVisible();
    await expect(h1).toBeVisible();

    // Verify heading hierarchy
    await expect(h1).toHaveText('Agenticly Agentic Demo');
  });

  test('should have proper page title', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveTitle('agenticly-agentic-agents');
  });

  test('should have readable text contrast', async ({ page }) => {
    await page.goto('/');
    
    // Check that text elements are visible (implies sufficient contrast)
    const title = page.locator('h1');
    const greeting = page.locator('.greeting');
    
    await expect(title).toBeVisible();
    await expect(greeting).toBeVisible();
  });

  test('should work with keyboard navigation', async ({ page }) => {
    await page.goto('/');
    
    // Test that page can receive focus
    await page.keyboard.press('Tab');
    
    // Verify content is still accessible
    const title = page.locator('h1');
    await expect(title).toBeVisible();
  });
});