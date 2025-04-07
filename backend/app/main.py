from fastapi import FastAPI

from app.routes import auth

app = FastAPI()

@app.get("/")
def read_root():
    """
    Root route for health checks or welcome message.
    """
    return {"message": "Welcome to the Renewable Energy Visualizer API!"}

# Include authentication routes
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
