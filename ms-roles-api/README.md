# MS Roles API

A FastAPI-based microservice that returns employee roles based on first names or last names (surnames).

## Features

- Get employee role by first name or last name
- RESTful API with multiple endpoints
- **Azure Cosmos DB integration with in-memory fallback**
- **Repository pattern with caching for optimal performance**
- **Secure configuration with environment variables**
- Containerized with Docker
- Automatic API documentation with Swagger UI
- Health check endpoint

## Data Storage

The API supports two data storage modes:

### 1. Cosmos DB Mode (Production)
When `USE_COSMOS_DB=true`, employee data is stored in Azure Cosmos DB with:
- **Secure connection** using Azure Cosmos DB SDK
- **Performance optimization** with in-memory caching (5-minute TTL by default)
- **Partition key** on `first_name` for efficient queries
- **Automatic retry logic** and error handling
- **Graceful fallback** to in-memory data if connection fails

### 2. In-Memory Mode (Development/Testing)
When `USE_COSMOS_DB=false` (default), employee data is stored in memory:
- No external dependencies required
- Fast local development and testing
- Same data structure as Cosmos DB

## Employee Data

The API contains the following employee mappings:
- Mary Bina - CSA Manager
- Vasilis Zisiadis - CSA Cloud&AI
- Dimitris Kotanis - CSA Infra
- Joanna Tsakona - CSAM
- Thanasis Ragos - CSA Security
- Konstantina Fotiadou - CSA Data&AI

## Endpoints

### GET /
Root endpoint with API information

### GET /health
Health check endpoint

### POST /get-role
Get role by first name (JSON body)
```json
{
  "first_name": "Mary"
}
```

### GET /get-role/{first_name}
Get role by first name (path parameter)
Example: `/get-role/Mary`

### GET /employees
List all employees and their roles

### POST /get-role-by-surname
Get role by last name (JSON body)
```json
{
  "last_name": "Kotanis"
}
```

### GET /get-role-by-surname/{last_name}
Get role by last name (path parameter)
Example: `/get-role-by-surname/Kotanis`

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```bash
cp .env.example .env
```

Key environment variables:

- `USE_COSMOS_DB`: Set to `true` to enable Cosmos DB, `false` for in-memory mode (default: `false`)
- `COSMOS_ENDPOINT`: Your Cosmos DB endpoint URL (required when `USE_COSMOS_DB=true`)
- `COSMOS_KEY`: Your Cosmos DB primary key (required when `USE_COSMOS_DB=true`)
- `COSMOS_DATABASE_NAME`: Database name (default: `employees-db`)
- `COSMOS_CONTAINER_NAME`: Container name (default: `employees`)
- `CACHE_TTL_SECONDS`: Cache time-to-live in seconds (default: `300`)

### Cosmos DB Setup

#### 1. Create Cosmos DB Resources

```bash
# Set variables
RESOURCE_GROUP="rg-agenticly-agentic-poc-"
LOCATION="eastus2"
ACCOUNT_NAME="cosmos-employees-$(date +%s)"

# Create Cosmos DB account (if not exists)
az cosmosdb create \
  --name $ACCOUNT_NAME \
  --resource-group $RESOURCE_GROUP \
  --default-consistency-level Session \
  --locations regionName=$LOCATION failoverPriority=0

# Get connection details
COSMOS_ENDPOINT=$(az cosmosdb show --name $ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query documentEndpoint -o tsv)
COSMOS_KEY=$(az cosmosdb keys list --name $ACCOUNT_NAME --resource-group $RESOURCE_GROUP --query primaryMasterKey -o tsv)

echo "COSMOS_ENDPOINT=$COSMOS_ENDPOINT"
echo "COSMOS_KEY=$COSMOS_KEY"
```

#### 2. Initialize Database with Employee Data

```bash
# Set environment variables
export USE_COSMOS_DB=true
export COSMOS_ENDPOINT="your-endpoint-here"
export COSMOS_KEY="your-key-here"

# Run initialization script
python init_cosmos_db.py
```

This script will:
- Create the database and container if they don't exist
- Seed initial employee data
- Verify the data was created successfully

## Running the API

### Using Python directly

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment (optional, defaults to in-memory mode):
```bash
cp .env.example .env
# Edit .env with your settings
```

3. Run the API:
```bash
python main.py
```

### Using Docker

1. Build the Docker image:
```bash
docker build -t ms-roles-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 ms-roles-api
```

### Using Docker Compose

```bash
docker-compose up --build
```

## Testing the API

Once running, the API will be available at `http://localhost:8000`

- Swagger UI documentation: `http://localhost:8000/docs`
- ReDoc documentation: `http://localhost:8000/redoc`

### Example requests:

1. Get role by POST request:
```bash
curl -X POST "http://localhost:8000/get-role" \
     -H "Content-Type: application/json" \
     -d '{"first_name": "Mary"}'
```

2. Get role by GET request:
```bash
curl "http://localhost:8000/get-role/Mary"
```

3. List all employees:
```bash
curl "http://localhost:8000/employees"
```

4. Get role by last name (POST request):
```bash
curl -X POST "http://localhost:8000/get-role-by-surname" \
     -H "Content-Type: application/json" \
     -d '{"last_name": "Kotanis"}'
```

5. Get role by last name (GET request):
```bash
curl "http://localhost:8000/get-role-by-surname/Kotanis"
```

## Response Format

All successful role queries return:
```json
{
  "first_name": "Mary",
  "role": "CSA Manager", 
  "full_name": "Mary Bina"
}
```

## Security Best Practices

### Cosmos DB Security

1. **Use Azure Key Vault** for storing Cosmos DB credentials:
   ```bash
   # Store credentials in Key Vault
   az keyvault secret set --vault-name <vault-name> --name cosmos-endpoint --value <endpoint>
   az keyvault secret set --vault-name <vault-name> --name cosmos-key --value <key>
   ```

2. **Use Azure Managed Identity** when running on Azure:
   - Enable system-assigned or user-assigned managed identity
   - Grant appropriate Cosmos DB roles to the identity
   - SDK will automatically use managed identity authentication

3. **Enable Cosmos DB Firewall**:
   ```bash
   # Restrict access to specific IP ranges
   az cosmosdb update --name $ACCOUNT_NAME --resource-group $RESOURCE_GROUP \
     --ip-range-filter "0.0.0.0/0"  # Replace with your IP ranges
   ```

4. **Use Private Endpoints** for production:
   - Deploy Cosmos DB with private endpoint in your VNet
   - Disable public network access

5. **Enable Diagnostic Logs**:
   ```bash
   # Send logs to Log Analytics workspace
   az monitor diagnostic-settings create \
     --name cosmos-logs \
     --resource <cosmos-resource-id> \
     --logs '[{"category": "DataPlaneRequests","enabled": true}]' \
     --workspace <log-analytics-workspace-id>
   ```

### Performance Optimization

1. **Caching**: The API implements automatic caching with configurable TTL (default 5 minutes)
2. **Connection Pooling**: Cosmos DB client uses connection pooling for optimal performance
3. **Partition Key Strategy**: Uses `first_name` as partition key for even distribution
4. **Request Units**: Configured with minimum 400 RU/s for cost optimization

### Testing

Run the test suite:
```bash
pytest test_main.py -v
```

The tests work with both in-memory and Cosmos DB modes.
