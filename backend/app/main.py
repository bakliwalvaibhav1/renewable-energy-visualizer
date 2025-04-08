from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # allow_origins=["http://localhost:5173"],  # React frontend dev URL (Vite)
    allow_origins=["http://localhost:3000"],  # React frontend dev URL (Docker)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    """
    Root route for health checks or welcome message.
    """
    return {"message": "Welcome to the Renewable Energy Visualizer API!"}

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
