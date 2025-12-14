# Project Management System

A multi-tenant project management tool built with Django + GraphQL backend and React + TypeScript frontend.

## Tech Stack

- **Backend**: Django 4.x, Graphene (GraphQL), Django Channels (WebSockets), PostgreSQL
- **Frontend**: React 18+, TypeScript, Apollo Client, TailwindCSS
- **Infrastructure**: Docker, Docker Compose

## Features

- ✅ Multi-tenant organization-based data isolation
- ✅ Project management with status tracking (Active, Completed, On Hold)
- ✅ Task board with drag-and-drop (Kanban style)
- ✅ Task comments for collaboration
- ✅ Real-time updates via WebSocket subscriptions
- ✅ Light/Dark theme with glassmorphism effects
- ✅ Responsive design for mobile and desktop
- ✅ GraphQL API with queries, mutations, and subscriptions

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd project-management-system
```

2. Start all services with a single command:
```bash
docker-compose up --build
```

3. Access the application:
   - Frontend: http://localhost:3000
   - GraphQL Playground: http://localhost:8000/graphql/
   - Django Admin: http://localhost:8000/admin/

The database will be automatically seeded with sample data including:
- Demo Organization with 4 projects
- Acme Corporation with 1 project
- Sample tasks and comments

## Project Structure

```
├── docker-compose.yml      # Docker orchestration
├── backend/                # Django backend
│   ├── config/            # Django settings
│   ├── core/              # Main app (models, schema, mutations)
│   └── requirements.txt   # Python dependencies
├── frontend/              # React frontend
│   ├── src/
│   │   ├── components/    # UI components
│   │   ├── pages/         # Page components
│   │   ├── graphql/       # GraphQL operations
│   │   └── context/       # React contexts
│   └── package.json       # Node dependencies
└── docs/                  # Documentation
```

## API Documentation

See [docs/API.md](docs/API.md) for complete GraphQL schema and examples.

## Development

### Running locally without Docker

**Backend:**
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_data
python manage.py runserver
```

**Frontend:**
```bash
cd frontend
npm install
npm run dev
```

### Environment Variables

See `.env.example` for available configuration options.

## Technical Summary

See [docs/TECHNICAL_SUMMARY.md](docs/TECHNICAL_SUMMARY.md) for architectural decisions and trade-offs.

