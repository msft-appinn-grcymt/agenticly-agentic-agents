import { defineConfig, devices } from '@playwright/test';

/**
 * @see https://playwright.dev/docs/test-configuration
 */
export default defineConfig({
  testDir: './tests',
  /* Run tests in files in parallel */
  fullyParallel: true,
  /* Fail the build on CI if you accidentally left test.only in the source code. */
  forbidOnly: !!process.env.CI, // eslint-disable-line no-undef
  /* Retry on CI only */
  retries: process.env.CI ? 2 : 0, // eslint-disable-line no-undef
  /* Opt out of parallel tests on CI. */
  workers: process.env.CI ? 1 : undefined, // eslint-disable-line no-undef
  /* Reporter to use. See https://playwright.dev/docs/test-reporters */
  reporter: process.env.CI ? 'github' : 'html', // eslint-disable-line no-undef
  /* Shared settings for all the projects below. See https://playwright.dev/docs/api/class-testoptions. */
  use: {
    /* Base URL to use in actions like `await page.goto('/')`. */
    baseURL: 'http://localhost:4173',
    /* Collect trace when retrying the failed test. See https://playwright.dev/docs/trace-viewer */
    trace: 'on-first-retry',
    /* Take screenshot on failure */
    screenshot: 'on',
    video: 'retain-on-failure',
    /* Connect to Azure Playwright Testing service when running in CI with service URL */
    ...(process.env.PLAYWRIGHT_SERVICE_URL && { // eslint-disable-line no-undef
      connectOptions: {
        wsEndpoint: process.env.PLAYWRIGHT_SERVICE_URL, // eslint-disable-line no-undef
      },
    }),
  },

  /* Configure projects for major browsers */
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    // Enable Firefox and Safari only in CI for comprehensive testing 
    // while keeping local development fast with just Chromium
    ...(process.env.CI // eslint-disable-line no-undef
      ? [
          {
            name: 'firefox',
            use: { ...devices['Desktop Firefox'] },
          },
          {
            name: 'webkit',
            use: { ...devices['Desktop Safari'] },
          },
        ]
      : []),
  ],

  /* Run your local dev server before starting the tests */
  webServer: {
    command: 'npm run preview',
    url: 'http://localhost:4173',
    reuseExistingServer: !process.env.CI, // eslint-disable-line no-undef
    timeout: 120 * 1000,
  },
});