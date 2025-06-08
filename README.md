# ML Prediction Service

A web application that provides ML model predictions with user authentication.

## Setup

### Prerequisites
- Python 3.8+
- Node.js 14+
- PostgreSQL

### Backend Setup

1. Create a PostgreSQL database named `ml_service`

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the FastAPI backend:
```bash
uvicorn app.main:app --reload
```

The backend will run on http://localhost:8000

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on http://localhost:3000

## Features

- User authentication (registration and login)
- ML model predictions updated every 5 minutes
- Real-time prediction display with timestamp
- Secure API endpoints
- Modern UI with Tailwind CSS

## API Endpoints

- POST `/register` - Register new user
- POST `/token` - Login and get access token
- GET `/prediction` - Get latest prediction (requires authentication)

## Environment Variables

Create a `.env` file in the root directory with:

```env
DATABASE_URL=postgresql://postgres:postgres@localhost/ml_service
SECRET_KEY=your-secret-key
TINKOFF_TOKEN=your-tinkoff-token
``` 