### Travel Planner

A RESTful API built with FastAPI to help travellers plan trips, manage the project and collect places to visit.
This project integrates with the public **Art Institute of Chicago API** to validate artworks and places.

### Getting Started

You can run this application either using Docker or locally via Python.

### Option 1: Using Docker (Recommended)

1. Make sure you have Docker and Docker Compose installed.
2. Run the following command in the root directory:
   ```bash
   docker-compose up --build
3. The API will be available at http://localhost:8000.

### Option 2: Local Setup

1. Create a virtual environment:
    ```bash
    python -m venv .venv
    source .venv/bin/activate (On Windows .venv\Scripts\activate)

2. Install the dependencies:
    ```bash
   pip install -r requirements.txt

3. Run the development server:
    ```bash
   uvicorn app.main:app --reload

### API Documentation

Once the application is running, navigate to the following URL in your browser to access the interactive API documentation. You can test all endpoints directly from here:

http://localhost:8000/docs