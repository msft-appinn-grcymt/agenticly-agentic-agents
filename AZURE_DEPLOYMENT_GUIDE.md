# Azure Deployment Quick Start Guide

This guide provides a quick reference for deploying the Agenticly Agentic Agents React application to Microsoft Azure.

## Files Included

- **README.md**: Comprehensive Azure deployment documentation
- **azure-deployment.json**: ARM template for automated deployment
- **deploy-to-azure.sh**: Automated deployment script
- **.github/workflows/azure-static-web-apps.yml**: GitHub Actions workflow template
- **public/staticwebapp.config.json**: Azure Static Web Apps configuration
- **.env.template**: Environment variables template

## Quick Deployment Options

### Option 1: One-Click Deployment (Recommended)

```bash
# Make sure you have Azure CLI installed and are logged in
az login

# Run the deployment script
./deploy-to-azure.sh
```

### Option 2: Azure CLI Manual Deployment

```bash
# Create resource group
az group create --name agenticly-rg --location "East US 2"

# Deploy using ARM template
az deployment group create \
  --resource-group agenticly-rg \
  --template-file azure-deployment.json
```

### Option 3: Azure Portal

1. Go to [Azure Portal](https://portal.azure.com)
2. Create new Static Web App
3. Connect to GitHub repository
4. Configure build settings:
   - App location: `/`
   - Output location: `dist`

## Prerequisites Checklist

- [ ] Azure subscription with appropriate permissions
- [ ] Azure CLI installed (version 2.40+)
- [ ] Node.js 18+ installed
- [ ] GitHub repository access
- [ ] Git configured locally

## Post-Deployment Steps

1. **Verify deployment**: Check the provided URL
2. **Configure custom domain** (optional): In Azure portal
3. **Set up monitoring**: Enable Application Insights
4. **Configure environment variables**: In Azure portal settings
5. **Review GitHub Actions**: Check workflow runs

## Support

For detailed documentation, see the complete Azure Deployment section in [README.md](./README.md).

## Application Screenshot

![Agenticly Agentic Demo](https://github.com/user-attachments/assets/cc56d271-1dd8-4c87-9c80-9d0bbbc66f36)

The application features a beautiful gradient header with "Agenticly Agentic Demo" text and displays "Hello Boss!" as the main content.