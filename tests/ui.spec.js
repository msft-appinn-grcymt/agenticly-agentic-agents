import { test, expect } from '@playwright/test';

test.describe('Agenticly Agentic Demo UI Tests', () => {
  test('should display the application correctly', async ({ page }) => {
    await page.goto('/');
    
    // Check that the page loads
    await expect(page).toHaveTitle('agenticly-agentic-agents');
    
    // Check that the header banner is visible and contains correct text
    const header = page.locator('header.banner');
    await expect(header).toBeVisible();
    
    const title = page.locator('header.banner h1');
    await expect(title).toBeVisible();
    await expect(title).toHaveText('Agenticly Agentic Demo');
    
    // Check that the banner icons are visible
    const leftIcon = page.locator('header.banner .banner-icon.left');
    const rightIcon = page.locator('header.banner .banner-icon.right');
    await expect(leftIcon).toBeVisible();
    await expect(rightIcon).toBeVisible();
    await expect(leftIcon).toHaveText('⚡');
    await expect(rightIcon).toHaveText('🚀');
    
    // Check that the main content is visible
    const mainContent = page.locator('main.main-content');
    await expect(mainContent).toBeVisible();
    
    // Check that the greeting is displayed
    const greeting = page.locator('main.main-content p.greeting');
    await expect(greeting).toBeVisible();
    await expect(greeting).toHaveText('Hello Boss!');
  });

  test('should have proper styling and layout', async ({ page }) => {
    await page.goto('/');

    // Check that the header has the expected gradient background
    const header = page.locator('header.banner');
    const headerStyles = await header.evaluate(el => getComputedStyle(el));
    
    // Verify the header has a background (gradient styling)
    expect(headerStyles.background).toBeTruthy();
    
    // Check that the main content is properly centered
    const greeting = page.locator('main.main-content p.greeting');
    const greetingStyles = await greeting.evaluate(el => getComputedStyle(el));
    
    // Verify text alignment
    expect(greetingStyles.textAlign).toBe('center');
  });

  test('should be responsive on mobile viewport', async ({ page }) => {
    // Set mobile viewport
    await page.setViewportSize({ width: 375, height: 812 });
    await page.goto('/');

    // Check that elements are still visible on mobile
    const header = page.locator('header.banner');
    const title = page.locator('header.banner h1');
    const greeting = page.locator('main.main-content p.greeting');

    await expect(header).toBeVisible();
    await expect(title).toBeVisible();
    await expect(greeting).toBeVisible();
    
    // Verify text content is preserved
    await expect(title).toHaveText('Agenticly Agentic Demo');
    await expect(greeting).toHaveText('Hello Boss!');
  });

  test('should have no console errors', async ({ page }) => {
    const consoleErrors = [];
    
    page.on('console', msg => {
      if (msg.type() === 'error') {
        consoleErrors.push(msg.text());
      }
    });

    await page.goto('/');
    
    // Wait a moment for any potential errors to surface
    await page.waitForTimeout(1000);
    
    // Verify no console errors occurred
    expect(consoleErrors).toHaveLength(0);
  });
});