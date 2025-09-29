#!/bin/bash

# Azure Deployment Script for Agenticly Agentic Agents
# This script automates the deployment process to Azure Static Web Apps

set -e

# Configuration
RESOURCE_GROUP="agenticly-rg"
APP_NAME="agenticly-agentic-demo"
LOCATION="East US 2"
REPO_URL="https://github.com/msft-appinn-grcymt/agenticly-agentic-agents"
BRANCH="main"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Azure deployment for Agenticly Agentic Agents${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    echo "Visit: https://docs.microsoft.com/en-us/cli/azure/install-azure-cli"
    exit 1
fi

# Check if user is logged in
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Azure. Please log in.${NC}"
    az login
fi

# Get current subscription
SUBSCRIPTION=$(az account show --query name --output tsv)
echo -e "${GREEN}📋 Using subscription: ${SUBSCRIPTION}${NC}"

# Create resource group if it doesn't exist
echo -e "${YELLOW}📁 Creating resource group: ${RESOURCE_GROUP}${NC}"
az group create --name "$RESOURCE_GROUP" --location "$LOCATION" --output table

# Build the application locally first
echo -e "${YELLOW}🔨 Building application locally...${NC}"
npm ci
npm run lint
npm run build

# Deploy using ARM template
echo -e "${YELLOW}🌐 Deploying Static Web App...${NC}"
DEPLOYMENT_OUTPUT=$(az deployment group create \
    --resource-group "$RESOURCE_GROUP" \
    --template-file azure-deployment.json \
    --parameters appName="$APP_NAME" location="$LOCATION" repositoryUrl="$REPO_URL" branch="$BRANCH" \
    --query 'properties.outputs.staticWebAppUrl.value' \
    --output tsv)

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
    echo -e "${GREEN}🌍 Your app is available at: https://${DEPLOYMENT_OUTPUT}${NC}"
    echo -e "${YELLOW}⚡ GitHub Actions workflow will be automatically created for continuous deployment.${NC}"
    echo -e "${YELLOW}📊 Configure custom domain and monitoring in the Azure portal.${NC}"
else
    echo -e "${RED}❌ Deployment failed. Please check the error messages above.${NC}"
    exit 1
fi

echo -e "${GREEN}🎉 Deployment process completed!${NC}"