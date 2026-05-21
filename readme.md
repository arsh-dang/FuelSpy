# FuelSpy

A full-stack application for tracking and comparing fuel prices across different stations.

## Project Structure

```
.
├── backend/              # FastAPI server
├── frontend/             # Next.js web application
├── k8s/                  # Kubernetes deployment configs
├── docker-compose.yml    # Local development orchestration
└── docker/               # Docker build contexts
```

## Technology Stack

### Backend
- **Runtime**: Python 3.12
- **Framework**: FastAPI (async)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Database Driver**: asyncpg

### Frontend
- **Framework**: Next.js 16.2.2
- **Language**: TypeScript + React

### Infrastructure
- **Database**: PostgreSQL (port 5432)
- **Orchestration**: Docker Compose for local development, Kubernetes for production

## Database Schema

### Tables
- `stations` - Fuel station information
- `fuel_types` - Types of fuel available
- `prices` - Current fuel prices
- `price_history` - Historical price data

The schema is managed using Alembic migrations located in `backend/alembic/`.



## Getting Started

### Prerequisites
- Docker and Docker Compose
- Python 3.12 (for local backend development)
- Node.js (for local frontend development)

### Running with Docker Compose

```bash
docker-compose up
```

This will start:
- Backend API on http://localhost:8000
- Frontend on http://localhost:3000
- PostgreSQL database on localhost:5432
- Redis cache on localhost:6379

### Running Locally

#### Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

#### Frontend
```bash
cd frontend/fuelspy
npm install
npm run dev
```

## API Endpoints

### Stations
- `GET /api/stations` - List all fuel stations
- `GET /api/stations/{id}` - Get station details
- `POST /api/stations` - Create a new station
- `PUT /api/stations/{id}` - Update station info
- `DELETE /api/stations/{id}` - Delete a station


## Deployment

### Kubernetes
Deployment configurations are available in the `k8s/` directory:

- `namespace.yaml` - Kubernetes namespace
- `postgres.yaml` - PostgreSQL deployment
- `backend.yaml` - Backend API deployment
- `frontend.yaml` - Frontend deployment
- `configmap.yaml` - Configuration settings
- `secrets.yaml` - Sensitive data
- `postgres-pvc.yaml` - Persistent volume for database

Deploy to cluster:
```bash
kubectl apply -f k8s/
```

### Cloud Build
The project includes a `cloudbuild.yaml` configuration for automated CI/CD pipelines.


