# Cosmos DB Migration Guide

## Overview

This document describes the migration of employee data from hardcoded values to Azure Cosmos DB, implementing enterprise-grade data storage with security and performance best practices.

## Architecture

### Repository Pattern

The implementation uses the **Repository Pattern** to abstract data access:

```
┌─────────────────┐
│   FastAPI App   │
│   (main.py)     │
└────────┬────────┘
         │
         │ uses
         ▼
┌─────────────────────────┐
│  Employee Repository    │
│  (employee_repository)  │
└────────┬────────────────┘
         │
         ├─────────────┐
         │             │
         ▼             ▼
┌──────────────┐  ┌──────────────┐
│  Cosmos DB   │  │  In-Memory   │
│   (Production)│  │  (Dev/Test)  │
└──────────────┘  └──────────────┘
```

### Key Components

1. **config.py**: Centralized configuration management
2. **employee_repository.py**: Data access layer with caching
3. **init_cosmos_db.py**: Database initialization script
4. **main.py**: FastAPI application (updated to use repository)

## Features

### 1. Dual-Mode Operation

**In-Memory Mode** (Default):
- No external dependencies
- Fast local development
- All tests work without Cosmos DB

**Cosmos DB Mode** (Production):
- Azure Cosmos DB backend
- Secure credential management
- High availability and scalability

### 2. Performance Optimization

- **In-memory caching**: 5-minute TTL (configurable)
- **Connection pooling**: Reuses Cosmos DB connections
- **Partition key strategy**: Efficient queries by first_name
- **Minimal RU consumption**: 400 RU/s baseline

### 3. Security Best Practices

- **Environment-based configuration**: No hardcoded credentials
- **Azure Key Vault integration** (recommended for production)
- **Managed Identity support**: Automatic authentication on Azure
- **Firewall rules**: Network-level security
- **Diagnostic logging**: Audit trail and monitoring

### 4. Resilience

- **Graceful degradation**: Falls back to in-memory if Cosmos DB fails
- **Retry logic**: Built into Azure Cosmos SDK
- **Health checks**: Monitor application status
- **Error handling**: Comprehensive exception management

## Migration Steps

### Step 1: Install Dependencies

```bash
cd ms-roles-api
pip install -r requirements.txt
```

New dependencies:
- `azure-cosmos==4.5.1`: Azure Cosmos DB SDK
- `python-dotenv==1.0.0`: Environment variable management

### Step 2: Create Cosmos DB Resources

#### Option A: Using Azure CLI

```bash
# Variables
RESOURCE_GROUP="rg-agenticly-agentic-poc-"
LOCATION="eastus2"
ACCOUNT_NAME="cosmos-employees-$(date +%s)"

# Create Cosmos DB account
az cosmosdb create \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --default-consistency-level Session \
  --locations regionName=$LOCATION failoverPriority=0 \
  --enable-automatic-failover false \
  --enable-multiple-write-locations false

# Get credentials
COSMOS_ENDPOINT=$(az cosmosdb show \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --query documentEndpoint -o tsv)

COSMOS_KEY=$(az cosmosdb keys list \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --query primaryMasterKey -o tsv)

echo "COSMOS_ENDPOINT=$COSMOS_ENDPOINT"
echo "COSMOS_KEY=$COSMOS_KEY"
```

#### Option B: Using Azure Portal

1. Navigate to [Azure Portal](https://portal.azure.com)
2. Search for "Azure Cosmos DB"
3. Click "Create" → "Azure Cosmos DB for NoSQL"
4. Configure:
   - **Subscription**: Select your subscription
   - **Resource Group**: `rg-agenticly-agentic-poc-`
   - **Account Name**: Unique name (e.g., `cosmos-employees-prod`)
   - **Location**: `East US 2`
   - **Capacity mode**: Provisioned throughput
   - **Apply Free Tier Discount**: Yes (if available)
5. Click "Review + Create"
6. Copy the **URI** and **Primary Key** from "Keys" section

### Step 3: Configure Environment Variables

```bash
# Copy the example file
cp .env.example .env

# Edit .env with your credentials
cat > .env << EOF
USE_COSMOS_DB=true
COSMOS_ENDPOINT=https://your-account.documents.azure.com:443/
COSMOS_KEY=your-primary-key-here
COSMOS_DATABASE_NAME=employees-db
COSMOS_CONTAINER_NAME=employees
CACHE_TTL_SECONDS=300
EOF
```

### Step 4: Initialize Database

```bash
# Set environment variables
export USE_COSMOS_DB=true
export COSMOS_ENDPOINT="your-endpoint"
export COSMOS_KEY="your-key"

# Run initialization script
python init_cosmos_db.py
```

Expected output:
```
============================================================
Cosmos DB Employee Database Initialization
============================================================
INFO:employee_repository:Successfully connected to Cosmos DB
INFO:__main__:Starting employee data seeding...
INFO:__main__:Created employee: Mary Bina
INFO:__main__:Created employee: Vasilis Zisiadis
...
INFO:__main__:Total employees in database: 6
✓ Initialization completed successfully!
```

### Step 5: Verify Migration

```bash
# Start the API
python main.py

# Test endpoints (in another terminal)
curl http://localhost:8000/employees
curl http://localhost:8000/get-role/mary
```

### Step 6: Run Tests

```bash
# Tests work with both in-memory and Cosmos DB modes
pytest test_main.py -v
```

## Production Deployment

### 1. Use Azure Key Vault

Store credentials securely:

```bash
# Create Key Vault (if not exists)
az keyvault create \
  --name kv-agenticly-prod \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION

# Store secrets
az keyvault secret set \
  --vault-name kv-agenticly-prod \
  --name cosmos-endpoint \
  --value "$COSMOS_ENDPOINT"

az keyvault secret set \
  --vault-name kv-agenticly-prod \
  --name cosmos-key \
  --value "$COSMOS_KEY"
```

Update application to retrieve from Key Vault:

```python
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()
client = SecretClient(vault_url="https://kv-agenticly-prod.vault.azure.net/", credential=credential)

COSMOS_ENDPOINT = client.get_secret("cosmos-endpoint").value
COSMOS_KEY = client.get_secret("cosmos-key").value
```

### 2. Enable Managed Identity

For applications running on Azure (App Service, Container Apps, AKS):

```bash
# Enable system-assigned managed identity
az webapp identity assign --name <app-name> --resource-group $RESOURCE_GROUP

# Grant Cosmos DB access
PRINCIPAL_ID=$(az webapp identity show --name <app-name> --resource-group $RESOURCE_GROUP --query principalId -o tsv)

az cosmosdb sql role assignment create \
  --account-name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --role-definition-name "Cosmos DB Built-in Data Contributor" \
  --principal-id $PRINCIPAL_ID \
  --scope "/"
```

Then remove `COSMOS_KEY` from environment variables - SDK will use managed identity automatically.

### 3. Configure Firewall

Restrict access to specific IP ranges:

```bash
# Example: Allow only Azure services
az cosmosdb update \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --enable-public-network true \
  --ip-range-filter "0.0.0.0"  # Azure services only

# Or allow specific IPs
az cosmosdb update \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --ip-range-filter "52.1.2.3,10.0.0.0/24"
```

### 4. Enable Monitoring

```bash
# Create Log Analytics workspace
az monitor log-analytics workspace create \
  --resource-group $RESOURCE_GROUP \
  --workspace-name law-agenticly-prod

# Get workspace ID
WORKSPACE_ID=$(az monitor log-analytics workspace show \
  --resource-group $RESOURCE_GROUP \
  --workspace-name law-agenticly-prod \
  --query id -o tsv)

# Enable diagnostic settings
az monitor diagnostic-settings create \
  --name cosmos-diagnostics \
  --resource $(az cosmosdb show --name $ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query id -o tsv) \
  --logs '[{"category": "DataPlaneRequests", "enabled": true}]' \
  --metrics '[{"category": "Requests", "enabled": true}]' \
  --workspace $WORKSPACE_ID
```

### 5. Docker Deployment

```bash
# Build image
docker build -t ms-roles-api:latest .

# Run with environment variables
docker run -d \
  -p 8000:8000 \
  -e USE_COSMOS_DB=true \
  -e COSMOS_ENDPOINT="$COSMOS_ENDPOINT" \
  -e COSMOS_KEY="$COSMOS_KEY" \
  --name ms-roles-api \
  ms-roles-api:latest
```

Or use docker-compose:

```bash
# Set environment variables in .env file
docker-compose up -d
```

## Cost Optimization

### 1. Right-Size Throughput

Start with minimum 400 RU/s and scale based on usage:

```bash
# Update container throughput
az cosmosdb sql container throughput update \
  --account-name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --database-name employees-db \
  --name employees \
  --throughput 400
```

### 2. Enable Autoscale (Optional)

For variable workloads:

```bash
az cosmosdb sql container throughput update \
  --account-name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --database-name employees-db \
  --name employees \
  --max-throughput 1000
```

### 3. Use Free Tier

Azure offers 400 RU/s and 5GB free per account:
- Enable "Apply Free Tier Discount" during account creation
- Suitable for development/testing and small production workloads

## Monitoring and Troubleshooting

### Application Logs

The application logs key events:

```
INFO:employee_repository:Successfully connected to Cosmos DB
INFO:employee_repository:Cache refreshed with 6 employees
ERROR:employee_repository:Failed to refresh cache from Cosmos DB: <error>
WARNING:employee_repository:Falling back to in-memory data
```

### Cosmos DB Metrics

Monitor in Azure Portal:
1. Navigate to your Cosmos DB account
2. Go to "Metrics"
3. Key metrics:
   - **Total Requests**: Request volume
   - **Total Request Units**: RU consumption
   - **Server Side Latency**: Query performance
   - **Availability**: Uptime percentage

### Common Issues

#### Issue: "Module not found: azure.cosmos"

**Solution**: Install dependencies:
```bash
pip install -r requirements.txt
```

#### Issue: "Failed to initialize Cosmos DB: Unauthorized"

**Solution**: Verify credentials:
```bash
# Check endpoint and key are correct
az cosmosdb keys list --name $ACCOUNT_NAME --resource-group $RESOURCE_GROUP
```

#### Issue: "Request rate is too large"

**Solution**: Increase RU/s or implement exponential backoff:
```bash
az cosmosdb sql container throughput update \
  --account-name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --database-name employees-db \
  --name employees \
  --throughput 800
```

## Rollback Plan

If issues occur, easily rollback to in-memory mode:

```bash
# Set environment variable
export USE_COSMOS_DB=false

# Or edit .env file
echo "USE_COSMOS_DB=false" > .env

# Restart application
python main.py
```

The application will continue working with the same data using in-memory storage.

## Summary

✅ **Migration Complete** - Employee data can now be stored in Cosmos DB
✅ **Backward Compatible** - In-memory mode still available
✅ **Security** - Credentials in environment variables, Key Vault ready
✅ **Performance** - Caching layer reduces Cosmos DB calls
✅ **Resilience** - Graceful fallback on errors
✅ **Monitoring** - Diagnostic logs and metrics available
✅ **Cost Optimized** - Minimum RU/s configuration

## Next Steps

1. **Production Deployment**: Deploy to Azure App Service or Container Apps
2. **Managed Identity**: Remove credentials, use managed identity
3. **Key Vault Integration**: Move secrets to Azure Key Vault
4. **Private Endpoints**: Secure network access to Cosmos DB
5. **Backup Strategy**: Configure Cosmos DB backup retention
6. **Load Testing**: Validate performance under production load
