# google oauth

A FastAPI application with Google OAuth authentication and SQLAlchemy ORM.

## Features

- Google OAuth 2.0 authentication
- JWT token-based authorization
- Async SQLAlchemy with PostgreSQL
- Comprehensive test suite with pytest
- CORS support for frontend integration

## Setup

### Prerequisites

- Python 3.12+
- PostgreSQL database
- Google OAuth credentials

### Installation

1. Clone the repository and navigate to the project directory
2. Create a virtual environment:
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows: env\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up environment variables. Create a `.env` file in the root directory:
   ```env
   DB_HOST=localhost
   DB_PORT=5432
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_NAME=your_db_name

   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   GOOGLE_REDIRECT_URI=http://localhost:8000/auth/google/callback

   SECRET_KEY=your_jwt_secret_key
   ```

### Google OAuth Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google+ API
4. Create OAuth 2.0 credentials
5. Add your redirect URI: `http://localhost:8000/auth/google/callback`
6. Copy the Client ID and Client Secret to your `.env` file

### Database Setup

1. Create a PostgreSQL database
2. Run the migrations:
   ```bash
   alembic upgrade head
   ```

## Running the Application

Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Authentication

- `GET /auth/google/login` - Get Google OAuth authorization URL
- `GET /auth/google/callback` - Handle OAuth callback and return JWT token
- `GET /auth/me` - Get current user info (requires authentication)

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Project Structure

```
├── app/
│   ├── auth/
│   │   ├── dependencies.py    # Authentication dependencies
│   │   ├── jwt.py            # JWT token handling
│   │   └── oauth.py          # Google OAuth client
│   ├── models/
│   │   └── user.py           # User database model
│   ├── routes/
│   │   └── auth.py           # Authentication routes
│   └── schemas/
│       └── user.py           # Pydantic schemas
├── core/
│   └── config.py             # Application configuration
├── db/
│   ├── base.py               # SQLAlchemy base
│   └── session.py            # Database session
├── tests/
│   ├── conftest.py           # Test configuration
│   ├── test_auth.py          # Authentication tests
│   └── test_routes.py        # Route tests
├── alembic/                  # Database migrations
├── main.py                   # FastAPI application
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Development

### Code Formatting

```bash
black .
isort .
flake8 .
```

### Database Migrations

Create a new migration:
```bash
alembic revision --autogenerate -m "Migration message"
```

Apply migrations:
```bash
alembic upgrade head
```
