#!/usr/bin/env node

/**
 * Validation script to ensure the UI testing setup is correct
 * Run with: node scripts/validate-setup.js
 */

import { readFileSync, existsSync } from 'fs';
import { join } from 'path';

const projectRoot = process.cwd(); // eslint-disable-line no-undef

console.log('🔍 Validating UI Testing Setup...\n');

// Check if required files exist
const requiredFiles = [
  'playwright.config.js',
  'tests/ui.spec.js',
  'tests/accessibility.spec.js', 
  'tests/performance.spec.js',
  '.github/workflows/ui-tests.yml',
  'package.json'
];

let allFilesExist = true;

for (const file of requiredFiles) {
  const filePath = join(projectRoot, file);
  if (existsSync(filePath)) {
    console.log(`✅ ${file} exists`);
  } else {
    console.log(`❌ ${file} is missing`);
    allFilesExist = false;
  }
}

// Check package.json for required scripts and dependencies
try {
  const packageJson = JSON.parse(readFileSync(join(projectRoot, 'package.json'), 'utf8'));
  
  console.log('\n📦 Package.json validation:');
  
  // Check for test scripts
  const requiredScripts = ['test:ui', 'test:ui:headed', 'test:ui:debug'];
  for (const script of requiredScripts) {
    if (packageJson.scripts && packageJson.scripts[script]) {
      console.log(`✅ Script "${script}" exists`);
    } else {
      console.log(`❌ Script "${script}" is missing`);
      allFilesExist = false;
    }
  }
  
  // Check for Playwright dependency
  if (packageJson.devDependencies && packageJson.devDependencies['@playwright/test']) {
    console.log('✅ @playwright/test dependency exists');
  } else {
    console.log('❌ @playwright/test dependency is missing');
    allFilesExist = false;
  }
  
} catch (error) {
  console.log('❌ Error reading package.json:', error.message);
  allFilesExist = false;
}

// Check GitHub workflow file
try {
  const workflowContent = readFileSync(join(projectRoot, '.github/workflows/ui-tests.yml'), 'utf8');
  
  console.log('\n🔄 GitHub Actions workflow validation:');
  
  if (workflowContent.includes('npx playwright install')) {
    console.log('✅ Playwright browser installation step exists');
  } else {
    console.log('❌ Playwright browser installation step is missing');
    allFilesExist = false;
  }
  
  if (workflowContent.includes('npm run test:ui')) {
    console.log('✅ Test execution step exists');
  } else {
    console.log('❌ Test execution step is missing');
    allFilesExist = false;
  }
  
} catch (error) {
  console.log('❌ Error reading workflow file:', error.message);
  allFilesExist = false;
}

console.log('\n' + '='.repeat(50));

if (allFilesExist) {
  console.log('🎉 UI Testing setup is complete and valid!');
  console.log('\nNext steps:');
  console.log('1. Run "npm run test:ui" to execute tests locally');
  console.log('2. Create a pull request to test the CI integration');
  console.log('3. UI tests will run automatically and must pass for PR approval');
  process.exit(0); // eslint-disable-line no-undef
} else {
  console.log('❌ UI Testing setup has issues that need to be resolved');
  process.exit(1); // eslint-disable-line no-undef
}