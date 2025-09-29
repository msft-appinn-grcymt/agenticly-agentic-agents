# Agenticly Agentic Agents

[![UI Tests](https://github.com/msft-appinn-grcymt/agenticly-agentic-agents/actions/workflows/ui-tests.yml/badge.svg)](https://github.com/msft-appinn-grcymt/agenticly-agentic-agents/actions/workflows/ui-tests.yml)

Featuring all the agenticly agentic features!

## Prerequisites

Before getting started with development, ensure your local environment meets the following requirements:

### Node.js Version Requirements

This project requires **Node.js version 20.19.0 or higher** (or Node.js 22.12.0+). The specific requirement comes from our build tool Vite 7.1.7.

#### Check Your Current Node.js Version

```bash
node --version
```

You should see output like `v20.19.0` or higher. If your version is lower than 20.19.0, you'll need to upgrade.

#### Installing or Upgrading Node.js

Choose one of the following methods to install or upgrade Node.js:

**Option 1: Official Node.js Installer (Recommended for beginners)**
1. Visit [nodejs.org](https://nodejs.org/)
2. Download the LTS version (Long Term Support)
3. Run the installer and follow the instructions
4. Restart your terminal and verify: `node --version`

**Option 2: Node Version Manager (NVM) - Recommended for developers**

*For macOS/Linux:*
```bash
# Install nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Restart terminal or run:
source ~/.bashrc

# Install and use Node.js 20 LTS
nvm install 20
nvm use 20

# Verify installation
node --version
```

*For Windows:*
```bash
# Install nvm-windows from: https://github.com/coreybutler/nvm-windows/releases
# Then run:
nvm install 20.19.0
nvm use 20.19.0
```

**Option 3: Package Managers**

*Using Homebrew (macOS):*
```bash
brew install node@20
```

*Using Chocolatey (Windows):*
```bash
choco install nodejs --version=20.19.0
```

*Using APT (Ubuntu/Debian):*
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs
```

#### Verify Installation

After installation, verify both Node.js and npm are working:

```bash
node --version  # Should show v20.19.0 or higher
npm --version   # Should show 10.0.0 or higher
```

### Additional Requirements

- **Git**: For version control and cloning the repository
- **Text Editor**: VS Code, WebStorm, or your preferred editor
- **Modern Browser**: Chrome, Firefox, Safari, or Edge for development

## First UI Implementation

This repository contains a React-based user interface for the Agenticly Agentic Demo application. The UI features a modern design with a gradient header banner and clean typography.

## Quick Start

**⚠️ Important**: Make sure you have Node.js 20.19.0+ installed before proceeding. Check with `node --version` or see [Prerequisites](#prerequisites) for installation instructions.

1. **Install dependencies:**
   ```bash
   npm install
   ```

2. **Start development server:**
   ```bash
   npm run dev
   ```

3. **Build for production:**
   ```bash
   npm run build
   ```

4. **Preview production build:**
   ```bash
   npm run preview
   ```

5. **Run linting:**
   ```bash
   npm run lint
   ```

6. **Run UI tests:**
   ```bash
   npm run test:ui
   ```

7. **Run UI tests in headed mode (with browser window):**
   ```bash
   npm run test:ui:headed
   ```

8. **Debug UI tests:**
   ```bash
   npm run test:ui:debug
   ```

## Features

- Modern React 19 application built with Vite
- Responsive design with gradient header banner
- Clean, professional styling
- ESLint configuration for code quality
- Fast development and build process
- **Comprehensive UI testing with Playwright**
- **Automated testing in CI/CD pipeline**

## Project Structure

- `src/App.jsx` - Main application component
- `src/App.css` - Application-specific styles
- `src/main.jsx` - Application entry point
- `public/` - Static assets
- `dist/` - Built application (generated)
- **`tests/` - UI tests written in Playwright**
- **`playwright.config.js` - Playwright test configuration**

## UI Components

The application currently includes:
- **Header Banner**: Displays "Agenticly Agentic Demo" with gradient background
- **Main Content**: Shows "Hello Boss!" greeting message

## Development

This project uses:
- React 19.1.1
- Vite 7.1.7 (build tool)
- ESLint (code linting)
- Modern ES modules
- **Playwright (UI testing framework)**

## UI Testing

The project includes comprehensive UI tests using Playwright that verify:

- **Application Functionality**: Tests verify that the application loads correctly and displays expected content
- **Visual Elements**: Validates the header banner with gradient background and "Agenticly Agentic Demo" text
- **Content Validation**: Ensures the "Hello Boss!" greeting is displayed properly
- **Responsive Design**: Tests mobile viewport compatibility
- **Error-Free Execution**: Monitors for console errors during page load

### Running Tests Locally

```bash
# Run all UI tests (headless)
npm run test:ui

# Run tests with browser window visible
npm run test:ui:headed

# Run tests in debug mode with step-by-step execution
npm run test:ui:debug
```

### CI/CD Integration

UI tests are **mandatory** for all pull requests:
- Tests automatically run on every PR
- PRs cannot be merged until all UI tests pass
- Test results and reports are available in GitHub Actions
- Failed tests generate detailed reports with screenshots

## Screenshot

![UI Demo](https://github.com/user-attachments/assets/d5ef3bcd-6ff5-4d51-aa4d-f4f014984b4c)

The interface features a beautiful gradient header with "Agenticly Agentic Demo" text and a centered "Hello Boss!" greeting below.

## Azure Deployment

This section provides comprehensive guidance for deploying the Agenticly Agentic Agents web application to Microsoft Azure using modern cloud-native approaches and best practices.

### Prerequisites

Before deploying to Azure, ensure you have the following:

#### Required Tools
- **Azure CLI** (version 2.40+): [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Node.js** (version 20.19.0+): See [Prerequisites](#prerequisites) section for installation instructions
- **Git**: For source code management
- **Azure subscription**: Active Azure subscription with appropriate permissions

#### Azure Permissions
Your Azure account needs:
- **Contributor** role on the subscription or resource group
- **Static Web Apps Contributor** role (for Azure Static Web Apps)
- **App Service Contributor** role (for Azure App Service deployment)

### Recommended Deployment Options

#### Option 1: Azure Static Web Apps (Recommended)

Azure Static Web Apps is the ideal platform for this React application, providing:
- Global CDN distribution
- Built-in CI/CD with GitHub Actions
- Automatic HTTPS certificates
- Custom domains support
- Staging environments for pull requests

##### Setup Steps

1. **Create Azure Static Web App**
   ```bash
   # Login to Azure
   az login
   
   # Create resource group
   az group create --name agenticly-rg --location "East US 2"
   
   # Create Static Web App
   az staticwebapp create \
     --name agenticly-agentic-demo \
     --resource-group agenticly-rg \
     --source https://github.com/msft-appinn-grcymt/agenticly-agentic-agents \
     --location "East US 2" \
     --branch main \
     --app-location "/" \
     --output-location "dist"
   ```

2. **Configure Build Settings**
   The Static Web App will automatically detect the Vite configuration and use these settings:
   - **App location**: `/` (root directory)
   - **Output location**: `dist`
   - **Build command**: `npm run build`

3. **GitHub Actions Integration**
   Azure automatically creates a GitHub Actions workflow in `.github/workflows/` for continuous deployment.

#### Option 2: Azure App Service

For applications requiring server-side processing or more advanced hosting features:

1. **Create App Service Plan**
   ```bash
   az appservice plan create \
     --name agenticly-plan \
     --resource-group agenticly-rg \
     --sku B1 \
     --is-linux
   ```

2. **Create Web App**
   ```bash
   az webapp create \
     --name agenticly-agentic-demo \
     --resource-group agenticly-rg \
     --plan agenticly-plan \
     --runtime "NODE|18-lts"
   ```

3. **Configure Deployment**
   ```bash
   az webapp deployment source config \
     --name agenticly-agentic-demo \
     --resource-group agenticly-rg \
     --repo-url https://github.com/msft-appinn-grcymt/agenticly-agentic-agents \
     --branch main \
     --manual-integration
   ```

### Best Practices

#### Security
- **Enable HTTPS only**: Always enforce HTTPS in production
- **Configure CORS**: Properly configure Cross-Origin Resource Sharing if needed
- **Environment Variables**: Store sensitive configuration in Azure Key Vault
- **Content Security Policy**: Implement CSP headers for XSS protection

#### Performance
- **CDN Integration**: Use Azure CDN for global content delivery
- **Compression**: Enable Gzip compression (automatically handled by Azure Static Web Apps)
- **Caching**: Configure appropriate cache headers
- **Bundle Optimization**: Leverage Vite's built-in optimization

#### Monitoring
- **Application Insights**: Enable Azure Application Insights for monitoring
- **Log Analytics**: Configure Log Analytics workspace for centralized logging
- **Alerts**: Set up alerts for application health and performance

#### Cost Optimization
- **Static Web Apps Free Tier**: Utilize the free tier for development/small applications
- **Resource Tagging**: Implement consistent tagging for cost tracking
- **Auto-scaling**: Configure appropriate scaling policies
- **Reserved Instances**: Consider reserved pricing for production workloads

### Environment Configuration

#### Development Environment
```bash
# Install dependencies
npm install

# Start development server
npm run dev
```

#### Production Build
```bash
# Build for production
npm run build

# Preview production build locally
npm run preview
```

#### Environment Variables
For environment-specific configuration, create `.env` files:

```env
# .env.production
VITE_API_URL=https://your-api.azurewebsites.net
VITE_APP_VERSION=1.0.0
```

### Continuous Integration/Continuous Deployment

#### GitHub Actions Workflow (Auto-generated)
Azure Static Web Apps automatically creates a workflow similar to:

```yaml
name: Azure Static Web Apps CI/CD

on:
  push:
    branches: [main]
  pull_request:
    types: [opened, synchronize, reopened, closed]
    branches: [main]

jobs:
  build_and_deploy_job:
    if: github.event_name == 'push' || (github.event_name == 'pull_request' && github.event.action != 'closed')
    runs-on: ubuntu-latest
    name: Build and Deploy Job
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: true
      - name: Build And Deploy
        id: builddeploy
        uses: Azure/static-web-apps-deploy@v1
        with:
          azure_static_web_apps_api_token: ${{ secrets.AZURE_STATIC_WEB_APPS_API_TOKEN }}
          repo_token: ${{ secrets.GITHUB_TOKEN }}
          action: "upload"
          app_location: "/"
          output_location: "dist"
```

### Custom Domain Configuration

1. **Add Custom Domain in Azure Portal**
2. **Configure DNS Records**
   ```
   Type: CNAME
   Name: www (or subdomain)
   Value: your-app.azurestaticapps.net
   ```
3. **SSL Certificate**: Automatically provisioned by Azure

### Troubleshooting

#### Common Issues
- **Node.js Version Incompatibility**: 
  - **Error**: `The engine "node" is incompatible with this module` or build failures
  - **Solution**: Ensure Node.js version 20.19.0+ is installed. Run `node --version` to check. See [Prerequisites](#prerequisites) for upgrade instructions.
- **Build Failures**: Check Node.js version compatibility and ensure all dependencies are installed with `npm ci`
- **Routing Issues**: Ensure SPA fallback is configured
- **Environment Variables**: Verify VITE_ prefix for client-side variables
- **Dependencies**: Use `npm ci` for consistent builds instead of `npm install`

#### Monitoring and Logs
```bash
# View deployment logs
az staticwebapp show --name agenticly-agentic-demo --resource-group agenticly-rg

# Stream logs (App Service)
az webapp log tail --name agenticly-agentic-demo --resource-group agenticly-rg
```

### Additional Resources

- [Azure Static Web Apps Documentation](https://docs.microsoft.com/en-us/azure/static-web-apps/)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html)
- [Azure App Service Documentation](https://docs.microsoft.com/en-us/azure/app-service/)
- [Azure Architecture Center](https://docs.microsoft.com/en-us/azure/architecture/)
