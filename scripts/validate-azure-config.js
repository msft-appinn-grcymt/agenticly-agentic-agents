#!/usr/bin/env node

/**
 * Validation script for Azure Playwright Testing service configuration
 * This script checks if the required environment variables and configuration
 * are properly set for Azure Playwright Testing service integration.
 */

import { existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const projectRoot = join(__dirname, '..');

console.log('🔍 Validating Azure Playwright Testing configuration...\n');

// Check for required configuration files
const requiredFiles = [
  'playwright.config.js',
  'playwright-azure.config.js',
  'package.json',
];

let allFilesExist = true;

console.log('📁 Checking required files:');
for (const file of requiredFiles) {
  const filePath = join(projectRoot, file);
  const exists = existsSync(filePath);
  
  console.log(`  ${exists ? '✅' : '❌'} ${file}`);
  
  if (!exists) {
    allFilesExist = false;
  }
}

// Check for required environment variables
const requiredEnvVars = [
  'PLAYWRIGHT_SERVICE_URL',
  'AZURE_CLIENT_ID', 
  'AZURE_TENANT_ID',
  'AZURE_SUBSCRIPTION_ID'
];

console.log('\n🔐 Checking environment variables:');
let allEnvVarsSet = true;

for (const envVar of requiredEnvVars) {
  const isSet = !!process.env[envVar]; // eslint-disable-line no-undef
  console.log(`  ${isSet ? '✅' : '⚠️'} ${envVar}${isSet ? ' (set)' : ' (not set - required for Azure service)'}`);
  
  if (!isSet) {
    allEnvVarsSet = false;
  }
}

// Check package.json for required scripts
console.log('\n📦 Checking npm scripts:');
try {
  const packageJsonPath = join(projectRoot, 'package.json');
  const packageJson = JSON.parse(readFileSync(packageJsonPath, 'utf8'));
  
  const requiredScripts = [
    'test:ui',
    'test:ui:azure',
    'test:ui:headed',
    'test:ui:debug'
  ];
  
  let allScriptsExist = true;
  
  for (const script of requiredScripts) {
    const exists = !!packageJson.scripts?.[script];
    console.log(`  ${exists ? '✅' : '❌'} ${script}`);
    
    if (!exists) {
      allScriptsExist = false;
    }
  }
  
  console.log('\n📊 Validation Summary:');
  console.log(`  Files: ${allFilesExist ? '✅ All required files present' : '❌ Missing files'}`);
  console.log(`  Environment Variables: ${allEnvVarsSet ? '✅ All set' : '⚠️ Some missing (ok for local development)'}`);
  console.log(`  NPM Scripts: ${allScriptsExist ? '✅ All scripts configured' : '❌ Missing scripts'}`);
  
  if (allFilesExist && allScriptsExist) {
    console.log('\n🎉 Configuration validation passed!');
    
    if (!allEnvVarsSet) {
      console.log('\n💡 Note: Environment variables are not set locally. This is normal.');
      console.log('   They will be provided by GitHub Actions secrets in CI/CD pipeline.');
      console.log('   To test Azure service locally, set PLAYWRIGHT_SERVICE_URL and Azure credentials.');
    }
    
    console.log('\n🚀 Ready to run tests:');
    console.log('   • Local tests: npm run test:ui');
    console.log('   • Azure service: npm run test:ui:azure (requires env vars)');
    
    process.exit(0); // eslint-disable-line no-undef
  } else {
    console.log('\n❌ Configuration validation failed!');
    process.exit(1); // eslint-disable-line no-undef
  }
  
} catch (error) {
  console.error('\n❌ Error reading package.json:', error.message);
  process.exit(1); // eslint-disable-line no-undef
}