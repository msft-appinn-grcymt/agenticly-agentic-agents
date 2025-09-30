# MS Roles API

A FastAPI-based microservice that returns employee roles based on first names.

## Features

- Get employee role by first name
- RESTful API with multiple endpoints
- Containerized with Docker
- Automatic API documentation with Swagger UI
- Health check endpoint

## Employee Data

The API contains the following employee mappings:
- Mary Bina - CSA Manager
- Vasilis Zisiadis - CSA Cloud&AI
- Dimitris Kotanis - CSA Infra
- Joanna Tsakona - CSAM
- Thanasis Ragos - CSA Security

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

## Running the API

### Using Python directly

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the API:
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

## Response Format

All successful role queries return:
```json
{
  "first_name": "Mary",
  "role": "CSA Manager", 
  "full_name": "Mary Bina"
}
```
