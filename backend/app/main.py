from app.routes.stations import app
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Allow frontend 
    allow_methods=["*"], # Allow all HTTP methods
    allow_headers=["*"], # Allow all headers
)