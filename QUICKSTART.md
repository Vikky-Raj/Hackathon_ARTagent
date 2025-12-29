# Quick Start Guide - ARTAgent with Docker

Get the project running locally in 3 simple steps!

## Prerequisites
- Docker and Docker Compose installed
- Git

## Step 1: Clone and Setup
```bash
git clone https://github.com/Vikky-Raj/Hackathon_ARTagent.git
cd Hackathon_ARTagent
cp .env.example .env
```

## Step 2: Start Services
```bash
docker compose up --build
```

This starts:
- PostgreSQL database (port 5432)
- Backend API (port 8010)
- Frontend UI (port 8080)

## Step 3: Access the Application

- **API Documentation**: http://localhost:8010/docs
- **Frontend**: http://localhost:8080
- **API Base**: http://localhost:8010/api/v1/

## That's It! 🎉

The application is now running locally with PostgreSQL database.

## Optional: Enable Azure Services

To enable voice and AI features, add your Azure credentials to `.env`:

```bash
# Edit .env file
nano .env

# Add these values
AZURE_OPENAI_ENDPOINT=your-azure-openai-endpoint
AZURE_OPENAI_KEY=your-key
AZURE_SPEECH_REGION=your-region
AZURE_SPEECH_KEY=your-key
```

Then restart:
```bash
docker compose restart backend
```

## Common Commands

```bash
# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild after code changes
docker compose up --build

# Access database
docker compose exec postgres psql -U postgres -d artagent
```

## Need Help?

- **Detailed Setup**: See [DOCKER_SETUP.md](DOCKER_SETUP.md)
- **Implementation Details**: See [INFRASTRUCTURE_SETUP_SUMMARY.md](INFRASTRUCTURE_SETUP_SUMMARY.md)
- **Troubleshooting**: See [DOCKER_SETUP.md#troubleshooting](DOCKER_SETUP.md#-troubleshooting)

## Next Steps

1. ✅ Project is running locally
2. 📝 Configure Azure services (optional)
3. 🔧 Set up database migrations
4. 🚀 Deploy to production
5. 🔐 Configure Key Vault for secrets
6. 🔄 Set up CI/CD pipeline

See the detailed documentation for guidance on each step.
