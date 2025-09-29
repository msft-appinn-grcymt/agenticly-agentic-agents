# Agenticly Agentic Agents

Featuring all the agenticly agentic features!

## First UI Implementation

This repository contains a React-based user interface for the Agenticly Agentic Demo application. The UI features a modern design with a gradient header banner and clean typography.

## Quick Start

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

## Features

- Modern React 19 application built with Vite
- Responsive design with gradient header banner
- Clean, professional styling
- ESLint configuration for code quality
- Fast development and build process

## Project Structure

- `src/App.jsx` - Main application component
- `src/App.css` - Application-specific styles
- `src/main.jsx` - Application entry point
- `public/` - Static assets
- `dist/` - Built application (generated)

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

## Screenshot

![UI Demo](https://github.com/user-attachments/assets/d5ef3bcd-6ff5-4d51-aa4d-f4f014984b4c)

The interface features a beautiful gradient header with "Agenticly Agentic Demo" text and a centered "Hello Boss!" greeting below.

## Azure Deployment

This section provides comprehensive guidance for deploying the Agenticly Agentic Agents web application to Microsoft Azure using modern cloud-native approaches and best practices.

### Prerequisites

Before deploying to Azure, ensure you have the following:

#### Required Tools
- **Azure CLI** (version 2.40+): [Install Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- **Node.js** (version 18+): [Install Node.js](https://nodejs.org/)
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
- **Build Failures**: Check Node.js version compatibility
- **Routing Issues**: Ensure SPA fallback is configured
- **Environment Variables**: Verify VITE_ prefix for client-side variables
- **Dependencies**: Use `npm ci` for consistent builds

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
