# Microservices Architecture with API Gateway using Python FastAPI

A microservices-based application built with Python FastAPI implementing 
the API Gateway pattern. This project was developed as part of IT4020 - 
Modern Topics in IT, Practical 3.

## Architecture
Client → API Gateway (Port 8000) → Student Service (Port 8001)

## Features
- Student microservice with full CRUD operations
- API Gateway for centralized request routing
- Auto-generated Swagger UI documentation
- JWT Authentication
- Request logging middleware
- Enhanced error handling

## How to Run

### 1. Clone the repository
git clone https://github.com/yourusername/microservices-fastapi.git
cd microservices-fastapi

### 2. Set up virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux

### 3. Install dependencies
pip install -r requirements.txt

### 4. Run Student Service
cd student-service
uvicorn main:app --reload --port 8001

### 5. Run API Gateway (new terminal)
cd gateway
uvicorn main:app --reload --port 8000

## API Documentation
- Student Service: http://localhost:8001/docs
- API Gateway: http://localhost:8000/docs

## Technologies Used
- Python 3.8+
- FastAPI
- Uvicorn
- HTTPx
- Pydantic
