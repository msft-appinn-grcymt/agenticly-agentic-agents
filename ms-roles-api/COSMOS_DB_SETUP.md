# Azure Cosmos DB Setup Guide

This guide provides step-by-step instructions for setting up Azure Cosmos DB for the MS Roles API.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Creating Cosmos DB Account](#creating-cosmos-db-account)
- [Configuration](#configuration)
- [Seeding Data](#seeding-data)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)

## Prerequisites

- Azure subscription with appropriate permissions
- Azure CLI installed and logged in
- Python 3.11+ installed
- pip package manager

## Creating Cosmos DB Account

### Option 1: Using Azure Portal

1. **Navigate to Azure Portal**
   - Go to https://portal.azure.com
   - Sign in with your Azure account

2. **Create Cosmos DB Account**
   - Click "Create a resource"
   - Search for "Azure Cosmos DB"
   - Select "Azure Cosmos DB" and click "Create"

3. **Configure Basic Settings**
   - **Subscription**: Select your subscription
   - **Resource Group**: `rg-agenticly-agentic-poc-` (or create new)
   - **Account Name**: Choose a unique name (e.g., `agenticly-employees-db`)
   - **API**: Select "Core (SQL)"
   - **Location**: Choose a region close to your users (e.g., East US 2)
   - **Capacity mode**: Serverless (recommended for development) or Provisioned throughput

4. **Configure Advanced Settings**
   - **Backup Policy**: Periodic (default)
   - **Network**: Public endpoint (for initial setup)
   - **Encryption**: Service-managed keys (default)

5. **Review and Create**
   - Review your settings
   - Click "Create"
   - Wait for deployment to complete (typically 5-10 minutes)

### Option 2: Using Azure CLI

```bash
# Set variables
SUBSCRIPTION_ID="6a450bf1-e243-4036-8210-822c2b95d3ad"
RESOURCE_GROUP="rg-agenticly-agentic-poc-"
ACCOUNT_NAME="agenticly-employees-db"
LOCATION="eastus2"

# Login to Azure
az login

# Set subscription
az account set --subscription $SUBSCRIPTION_ID

# Create Cosmos DB account
az cosmosdb create \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --default-consistency-level Session \
  --locations regionName=$LOCATION failoverPriority=0 isZoneRedundant=False \
  --enable-automatic-failover false \
  --capabilities EnableServerless

# Wait for account to be ready
az cosmosdb show \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --query provisioningState
```

## Configuration

### 1. Get Cosmos DB Connection Information

#### Using Azure Portal:
1. Navigate to your Cosmos DB account
2. Go to "Keys" under Settings
3. Copy the following:
   - **URI** (Cosmos DB Endpoint)
   - **PRIMARY KEY**

#### Using Azure CLI:
```bash
# Get endpoint
az cosmosdb show \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --query documentEndpoint -o tsv

# Get primary key
az cosmosdb keys list \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --query primaryMasterKey -o tsv
```

### 2. Configure Environment Variables

1. **Copy the example environment file**:
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` file** with your Cosmos DB credentials:
   ```env
   USE_COSMOS_DB=true
   COSMOS_ENDPOINT=https://your-account-name.documents.azure.com:443/
   COSMOS_KEY=your-primary-key-here
   COSMOS_DATABASE_NAME=employees-db
   COSMOS_CONTAINER_NAME=employees
   ```

3. **Secure the `.env` file**:
   ```bash
   chmod 600 .env
   ```

### 3. For Docker Deployment

**Option A: Environment Variables**
```bash
docker run -p 8000:8000 \
  -e USE_COSMOS_DB=true \
  -e COSMOS_ENDPOINT="https://your-account.documents.azure.com:443/" \
  -e COSMOS_KEY="your-primary-key" \
  -e COSMOS_DATABASE_NAME="employees-db" \
  -e COSMOS_CONTAINER_NAME="employees" \
  ms-roles-api
```

**Option B: Environment File**
```bash
docker run -p 8000:8000 --env-file .env ms-roles-api
```

### 4. For Azure Container Apps / App Service

Set application settings in Azure Portal:
- `USE_COSMOS_DB` = `true`
- `COSMOS_ENDPOINT` = `https://your-account.documents.azure.com:443/`
- `COSMOS_KEY` = `your-primary-key`
- `COSMOS_DATABASE_NAME` = `employees-db`
- `COSMOS_CONTAINER_NAME` = `employees`

**Using Azure CLI**:
```bash
az webapp config appsettings set \
  --name your-app-name \
  --resource-group $RESOURCE_GROUP \
  --settings \
    USE_COSMOS_DB=true \
    COSMOS_ENDPOINT="https://your-account.documents.azure.com:443/" \
    COSMOS_KEY="your-primary-key" \
    COSMOS_DATABASE_NAME="employees-db" \
    COSMOS_CONTAINER_NAME="employees"
```

## Seeding Data

### Initialize Database with Employee Data

1. **Ensure environment is configured**:
   ```bash
   cat .env  # Verify configuration
   ```

2. **Run the seed script**:
   ```bash
   python seed_database.py
   ```

3. **Expected Output**:
   ```
   ============================================================
     Employee Database Seeding Script
   ============================================================
   
   ✅ Environment variables loaded from .env file
   
   🚀 Starting database seed...
      Database: employees-db
      Container: employees
   
   ✅ Created: Mary Bina - CSA Manager
   ✅ Created: Vasilis Zisiadis - CSA Cloud&AI
   ✅ Created: Dimitris Kotanis - CSA Infra
   ✅ Created: Joanna Tsakona - CSAM
   ✅ Created: Thanasis Ragos - CSA Security
   ✅ Created: Konstantina Fotiadou - CSA Data&AI
   
   ============================================================
   ✅ Successfully seeded: 6 employees
   ============================================================
   
   🔍 Verifying seeded data...
      Total employees in database: 6
   
   📋 Employee List:
      • Mary Bina: CSA Manager
      • Vasilis Zisiadis: CSA Cloud&AI
      • Dimitris Kotanis: CSA Infra
      • Joanna Tsakona: CSAM
      • Thanasis Ragos: CSA Security
      • Konstantina Fotiadou: CSA Data&AI
   
   🎉 Database seeding completed successfully!
   ```

### Manual Data Addition via Azure Portal

1. Navigate to your Cosmos DB account
2. Go to "Data Explorer"
3. Expand "employees-db" database
4. Expand "employees" container
5. Click "New Item"
6. Add employee JSON:
   ```json
   {
     "id": "john",
     "first_name": "john",
     "last_name": "doe",
     "full_name": "John Doe",
     "role": "Software Engineer"
   }
   ```

## Security Best Practices

### 1. Use Azure Key Vault for Secrets

**Store Cosmos DB Key in Key Vault**:
```bash
# Create Key Vault
az keyvault create \
  --name kv-agenticly-agentic \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Store Cosmos DB key
COSMOS_KEY=$(az cosmosdb keys list \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --query primaryMasterKey -o tsv)

az keyvault secret set \
  --vault-name kv-agenticly-agentic \
  --name cosmos-primary-key \
  --value "$COSMOS_KEY"
```

### 2. Use Managed Identity (Production)

For production deployments, use Azure Managed Identity instead of keys:

```python
# Example code for managed identity
from azure.identity import DefaultAzureCredential
from azure.cosmos import CosmosClient

credential = DefaultAzureCredential()
client = CosmosClient(url=endpoint, credential=credential)
```

### 3. Network Security

**Restrict Access to Specific IPs**:
```bash
az cosmosdb update \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --ip-range-filter "YOUR_APP_IP/32"
```

**Enable Virtual Network Service Endpoints** (for Azure-hosted apps):
```bash
az cosmosdb update \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --enable-virtual-network true \
  --virtual-network-rules "SUBNET_ID"
```

### 4. Enable Diagnostic Logging

```bash
az monitor diagnostic-settings create \
  --name cosmos-diagnostics \
  --resource $COSMOS_DB_RESOURCE_ID \
  --logs '[{"category": "DataPlaneRequests","enabled": true}]' \
  --metrics '[{"category": "Requests","enabled": true}]' \
  --workspace $LOG_ANALYTICS_WORKSPACE_ID
```

## Performance Optimization

### 1. Indexing Policy

The application automatically configures optimized indexing for:
- `first_name` (for fast first name queries)
- `last_name` (for fast surname queries)
- `role` (for filtering by role)

### 2. Caching Strategy

The repository implements intelligent caching:
- Employee data is cached after first load
- Cache is invalidated on data updates
- Reduces Cosmos DB RU consumption

### 3. Query Optimization

- Uses parameterized queries to prevent SQL injection
- Implements case-insensitive searches efficiently
- Minimizes cross-partition queries

## Monitoring and Troubleshooting

### Check Cosmos DB Metrics

**Using Azure Portal**:
1. Navigate to Cosmos DB account
2. Click on "Metrics"
3. Monitor:
   - Request Units (RU/s)
   - Total Requests
   - Storage Used
   - Latency

**Using Azure CLI**:
```bash
az monitor metrics list \
  --resource $COSMOS_DB_RESOURCE_ID \
  --metric "TotalRequests" \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-01-02T00:00:00Z
```

### Common Issues

#### Issue: "Connection timeout"
**Solution**: 
- Check firewall settings
- Verify endpoint URL is correct
- Ensure network connectivity

#### Issue: "Unauthorized" or "Invalid credentials"
**Solution**:
- Verify COSMOS_KEY is correct
- Check key hasn't been regenerated
- Ensure proper environment variable configuration

#### Issue: "Container not found"
**Solution**:
- Run seed script to create database and container
- Verify COSMOS_DATABASE_NAME and COSMOS_CONTAINER_NAME

#### Issue: "High RU consumption"
**Solution**:
- Review query patterns
- Implement caching
- Optimize indexing policy
- Consider upgrading to provisioned throughput

### Enable Debug Logging

Add to your application:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Cost Management

### Serverless Pricing (Recommended for Development)
- Pay per request (RU/s)
- No minimum charge
- Best for variable workloads

### Provisioned Throughput (Production)
- Reserve RU/s capacity
- Predictable costs
- Better for consistent workloads

### Cost Optimization Tips
1. Use caching to reduce queries
2. Implement efficient indexing
3. Clean up unused data
4. Use serverless for dev/test
5. Monitor and set budget alerts

## Additional Resources

- [Azure Cosmos DB Documentation](https://docs.microsoft.com/azure/cosmos-db/)
- [Cosmos DB Python SDK](https://docs.microsoft.com/python/api/azure-cosmos/)
- [Cosmos DB Best Practices](https://docs.microsoft.com/azure/cosmos-db/best-practice-dotnet)
- [Cosmos DB Pricing](https://azure.microsoft.com/pricing/details/cosmos-db/)
- [Azure Key Vault](https://docs.microsoft.com/azure/key-vault/)

## Support

For issues or questions:
1. Check the [Troubleshooting](#monitoring-and-troubleshooting) section
2. Review Azure Cosmos DB logs in Azure Portal
3. Contact your Azure administrator
4. Open an issue in the repository
