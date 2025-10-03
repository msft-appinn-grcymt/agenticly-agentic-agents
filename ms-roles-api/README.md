# MS Roles API

A FastAPI-based microservice that returns employee roles based on first names or last names (surnames).

## Features

- Get employee role by first name or last name
- RESTful API with multiple endpoints
- Containerized with Docker
- Automatic API documentation with Swagger UI
- Health check endpoint

## Employee Data

**Data Storage:** Employee data is now dynamically stored in Azure Cosmos DB with automatic fallback to in-memory data for local development.

The API contains the following employee mappings:
- Mary Bina - CSA Manager
- Vasilis Zisiadis - CSA Cloud&AI
- Dimitris Kotanis - CSA Infra
- Joanna Tsakona - CSAM
- Thanasis Ragos - CSA Security
- Konstantina Fotiadou - CSA Data&AI

### Cosmos DB Integration

The API uses Azure Cosmos DB for persistent storage with the following benefits:
- **Dynamic Data**: Add/update employees without code changes
- **High Availability**: Azure Cosmos DB SLA guarantees
- **Performance**: Optimized indexing for fast queries
- **Scalability**: Automatic scaling as data grows
- **Security**: Connection via environment variables

#### Configuration

1. **Create `.env` file** from the template:
   ```bash
   cp .env.example .env
   ```

2. **Configure Cosmos DB** in `.env`:
   ```env
   USE_COSMOS_DB=true
   COSMOS_ENDPOINT=https://your-account.documents.azure.com:443/
   COSMOS_KEY=your-primary-key
   COSMOS_DATABASE_NAME=employees-db
   COSMOS_CONTAINER_NAME=employees
   ```

3. **Seed the database** with initial employee data:
   ```bash
   python seed_database.py
   ```

#### Local Development Mode

For local development without Cosmos DB:
```env
USE_COSMOS_DB=false
```

The API will automatically use in-memory fallback data with the same employee records.

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

## Running the API

### Using Python directly

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. (Optional) Configure Cosmos DB:
```bash
cp .env.example .env
# Edit .env with your Cosmos DB credentials
```

3. (Optional) Seed the database:
```bash
python seed_database.py
```

4. Run the API:
```bash
python main.py
```

The API will start on `http://localhost:8000` using either Cosmos DB or in-memory data based on your configuration.

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
