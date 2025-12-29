# Local Development Setup with Docker

This guide explains how to run the ARTAgent project locally using Docker with PostgreSQL database.

## 🚀 Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git (to clone the repository)

### Step 1: Clone and Configure

```bash
# Clone the repository (if not already done)
git clone https://github.com/Vikky-Raj/Hackathon_ARTagent.git
cd Hackathon_ARTagent

# Create your environment file from the template
cp .env.example .env
```

### Step 2: Configure Environment Variables

Edit the `.env` file and configure at minimum:

```bash
# Required for basic operation
ENVIRONMENT=development
DEBUG_MODE=true
BASE_URL=http://localhost:8010

# Database (already configured for Docker)
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=artagent
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

# Optional: Add Azure service credentials if you want to use voice/AI features
# AZURE_OPENAI_ENDPOINT=your-endpoint
# AZURE_OPENAI_KEY=your-key
# etc.
```

**Note:** For local development without Azure services, the backend will run but voice and AI features will be disabled. This is perfect for working on the Tool Registry platform features.

### Step 3: Start All Services

```bash
# Build and start all services (backend, frontend, PostgreSQL)
docker compose up --build
```

This command will:
- Build the backend Docker image (Python 3.11)
- Build the frontend Docker image
- Start a PostgreSQL 15 database container
- Connect all services together
- Make services available at:
  - Backend API: http://localhost:8010
  - Frontend: http://localhost:8080
  - PostgreSQL: localhost:5432

### Step 4: Verify Setup

Once all containers are running, you can verify:

```bash
# Check container status
docker compose ps

# View backend logs
docker compose logs backend

# View database logs
docker compose logs postgres

# Access the API docs
# Open http://localhost:8010/docs in your browser
```

## 🗃️ Database Management

### Connect to PostgreSQL

```bash
# Using docker compose exec
docker compose exec postgres psql -U postgres -d artagent

# Or using psql from your host (if installed)
psql -h localhost -p 5432 -U postgres -d artagent
```

### Database Migrations

The project is set up to use PostgreSQL. To add database migrations:

1. Add your preferred migration tool (Alembic, Django migrations, etc.) to `requirements.txt`
2. Create migration scripts
3. Run migrations on container startup or manually

Example with Alembic:
```bash
# Install Alembic
docker compose exec backend pip install alembic

# Initialize Alembic (one-time)
docker compose exec backend alembic init migrations

# Create a migration
docker compose exec backend alembic revision --autogenerate -m "Initial schema"

# Run migrations
docker compose exec backend alembic upgrade head
```

## 🔧 Development Workflow

### Making Code Changes

The Docker setup uses bind mounts for development, so code changes are reflected immediately:

1. Edit files in your local repository
2. The backend service will auto-reload (if uvicorn reload is enabled)
3. Refresh your browser to see changes

### Rebuilding After Dependency Changes

If you modify `requirements.txt`:

```bash
# Rebuild backend container
docker compose up --build backend
```

### Stopping Services

```bash
# Stop all services (keeps data)
docker compose down

# Stop and remove all data (including database)
docker compose down -v
```

### Viewing Logs

```bash
# All services
docker compose logs -f

# Specific service
docker compose logs -f backend
docker compose logs -f postgres
```

## 📦 Project Structure

```
.
├── docker-compose.yml          # Multi-container orchestration
├── .env.example               # Environment template
├── .env                       # Your local config (git-ignored)
├── apps/
│   └── rtagent/
│       ├── backend/
│       │   ├── Dockerfile     # Backend container definition
│       │   ├── main.py       # FastAPI application entry
│       │   └── config/
│       │       ├── database_config.py  # PostgreSQL config
│       │       └── ...
│       └── frontend/
│           └── Dockerfile     # Frontend container definition
├── src/                       # Core application code
└── requirements.txt           # Python dependencies
```

## 🌩️ Integrating Azure Services

### For Development

The application supports both local and cloud operation:

1. **Local-only mode** (current setup):
   - Uses PostgreSQL for data
   - No Azure services required
   - Perfect for Tool Registry development

2. **Hybrid mode** (local app + cloud services):
   - Add Azure credentials to `.env`
   - Application connects to Azure OpenAI, Speech, ACS
   - Database remains local

3. **Full cloud mode**:
   - Deploy using Azure Container Apps (see deployment docs)
   - All services run in Azure

### Adding Azure Services

To enable Azure services for voice and AI features, add to your `.env`:

```bash
# Azure OpenAI (for LLM)
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com
AZURE_OPENAI_KEY=your-key
AZURE_OPENAI_CHAT_DEPLOYMENT_ID=gpt-4

# Azure Speech (for STT/TTS)
AZURE_SPEECH_REGION=eastus
AZURE_SPEECH_KEY=your-key

# Azure Communication Services (for telephony)
ACS_ENDPOINT=https://your-acs.communication.azure.com
ACS_CONNECTION_STRING=your-connection-string
```

See `.env.example` for complete list of available Azure configurations.

## 🔐 Production Secrets Management

For production deployments, never commit secrets to `.env`. Instead:

### Option 1: Azure Key Vault (Recommended)

```bash
# Store secrets in Key Vault
az keyvault secret set --vault-name your-vault --name POSTGRES-PASSWORD --value "your-secure-password"

# Application code can retrieve secrets using Azure SDK
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

client = SecretClient(vault_url="https://your-vault.vault.azure.net", credential=DefaultAzureCredential())
secret = client.get_secret("POSTGRES-PASSWORD")
```

### Option 2: Environment Variables (CI/CD)

In your CI/CD pipeline (GitHub Actions, Azure DevOps):

```yaml
# .github/workflows/deploy.yml
env:
  POSTGRES_PASSWORD: ${{ secrets.POSTGRES_PASSWORD }}
  AZURE_OPENAI_KEY: ${{ secrets.AZURE_OPENAI_KEY }}
```

### Option 3: Docker Secrets (Docker Swarm/Kubernetes)

```bash
# Create secret
echo "my-secure-password" | docker secret create postgres_password -

# Use in docker-compose.yml
services:
  backend:
    secrets:
      - postgres_password
```

## 🚀 CI/CD Pipeline Integration

### GitHub Actions Example

Create `.github/workflows/docker-build.yml`:

```yaml
name: Build and Push Docker Images

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ secrets.CONTAINER_REGISTRY }}
          username: ${{ secrets.REGISTRY_USERNAME }}
          password: ${{ secrets.REGISTRY_PASSWORD }}
      
      - name: Build and push backend
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./apps/rtagent/backend/Dockerfile
          push: true
          tags: ${{ secrets.CONTAINER_REGISTRY }}/artagent-backend:${{ github.sha }}
```

### Azure Container Apps Deployment

```bash
# Build and push to Azure Container Registry
az acr build --registry your-registry --image artagent-backend:latest \
  --file ./apps/rtagent/backend/Dockerfile .

# Deploy to Container Apps
az containerapp update \
  --name artagent-backend \
  --resource-group your-rg \
  --image your-registry.azurecr.io/artagent-backend:latest
```

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Check what's using the port
lsof -i :8010  # or :5432

# Change ports in .env
BACKEND_PORT=8011
```

### Database Connection Issues

```bash
# Check if postgres is healthy
docker compose ps

# Check postgres logs
docker compose logs postgres

# Verify connection from backend
docker compose exec backend ping postgres
```

### Backend Not Starting

```bash
# Check logs for errors
docker compose logs backend

# Rebuild without cache
docker compose build --no-cache backend
docker compose up backend
```

### Permission Errors

```bash
# Fix file permissions
sudo chown -R $USER:$USER .

# Rebuild containers
docker compose down
docker compose up --build
```

## 📚 Next Steps

- [ ] Set up database migrations (Alembic recommended)
- [ ] Configure Azure services for voice features
- [ ] Set up CI/CD pipeline
- [ ] Deploy to Azure Container Apps for production
- [ ] Configure Key Vault for production secrets
- [ ] Set up monitoring and logging

## 📖 Additional Resources

- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [PostgreSQL Docker Image](https://hub.docker.com/_/postgres)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/)
- [Azure Key Vault](https://learn.microsoft.com/azure/key-vault/)
