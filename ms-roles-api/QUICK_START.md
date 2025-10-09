# Quick Start Guide - Cosmos DB Migration

## TL;DR

The MS Roles API now supports Azure Cosmos DB for employee data storage while maintaining backward compatibility with in-memory mode.

## Development Mode (Default)

No changes required! The API works out-of-the-box with in-memory data:

```bash
cd ms-roles-api
pip install -r requirements.txt
python main.py
```

All existing tests pass:
```bash
pytest test_main.py -v
```

## Production Mode (Cosmos DB)

### 1. Create Cosmos DB Account

Using Azure CLI:
```bash
RESOURCE_GROUP="rg-agenticly-agentic-poc-"
ACCOUNT_NAME="cosmos-employees-prod"

az cosmosdb create \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --default-consistency-level Session \
  --locations regionName=eastus2 failoverPriority=0
```

### 2. Configure Environment

```bash
# Copy template
cp .env.example .env

# Get credentials
COSMOS_ENDPOINT=$(az cosmosdb show --name $ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query documentEndpoint -o tsv)
COSMOS_KEY=$(az cosmosdb keys list --name $ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query primaryMasterKey -o tsv)

# Update .env
cat > .env << EOF
USE_COSMOS_DB=true
COSMOS_ENDPOINT=$COSMOS_ENDPOINT
COSMOS_KEY=$COSMOS_KEY
COSMOS_DATABASE_NAME=employees-db
COSMOS_CONTAINER_NAME=employees
CACHE_TTL_SECONDS=300
EOF
```

### 3. Initialize Database

```bash
python init_cosmos_db.py
```

### 4. Start API

```bash
python main.py
```

## Docker Deployment

### Development
```bash
docker-compose up
```

### Production
```bash
docker run -d \
  -p 8000:8000 \
  -e USE_COSMOS_DB=true \
  -e COSMOS_ENDPOINT="<your-endpoint>" \
  -e COSMOS_KEY="<your-key>" \
  ms-roles-api:latest
```

## Environment Variables

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `USE_COSMOS_DB` | No | `false` | Enable Cosmos DB mode |
| `COSMOS_ENDPOINT` | Yes* | - | Cosmos DB endpoint URL |
| `COSMOS_KEY` | Yes* | - | Cosmos DB primary key |
| `COSMOS_DATABASE_NAME` | No | `employees-db` | Database name |
| `COSMOS_CONTAINER_NAME` | No | `employees` | Container name |
| `CACHE_TTL_SECONDS` | No | `300` | Cache TTL in seconds |

*Required only when `USE_COSMOS_DB=true`

## Key Features

✅ **Zero Breaking Changes**: Existing API endpoints work identically  
✅ **Backward Compatible**: Falls back to in-memory data automatically  
✅ **Performance**: Built-in caching reduces database calls  
✅ **Security**: Environment-based credential management  
✅ **Resilience**: Graceful error handling and fallback  

## Testing

All existing tests pass with both modes:

```bash
# In-memory mode (default)
pytest test_main.py -v

# Cosmos DB mode (if configured)
export USE_COSMOS_DB=true
pytest test_main.py -v
```

## Troubleshooting

**Issue**: Module not found: `azure.cosmos`  
**Fix**: `pip install -r requirements.txt`

**Issue**: API still uses in-memory data  
**Fix**: Set `USE_COSMOS_DB=true` in `.env` file

**Issue**: Connection failed  
**Fix**: Verify `COSMOS_ENDPOINT` and `COSMOS_KEY` are correct

## More Information

- [Full Migration Guide](./COSMOS_DB_MIGRATION.md) - Complete documentation
- [README](./README.md) - API documentation and examples
- [Cosmos DB Documentation](https://docs.microsoft.com/azure/cosmos-db/)

## Support

For issues or questions, see [COSMOS_DB_MIGRATION.md](./COSMOS_DB_MIGRATION.md) for detailed troubleshooting.
