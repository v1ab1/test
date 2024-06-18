from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from core.config import settings
from core.models import Base, db_helper
from api_v1 import router as router_v1
from auth import router as auth_router
from logic.predict import update_predictions
import threading

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

# CORS middleware setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this to only the domains you want to allow
    allow_credentials=True,
    allow_methods=["*"],  # Adjust this to only the HTTP methods you want to allow
    allow_headers=["*"],  # Adjust this to only the HTTP headers you want to allow
)

# Include routers
app.include_router(router=router_v1, prefix=settings.api_v1_prefix)
app.include_router(router=auth_router)

# Function to prepare data (called in a separate thread)
def prepare():
    print('Started prediction')
    update_predictions(2024, 40)

# Start preparation process in a separate thread
# threading.Thread(target=prepare).start()

# Route for homepage
@app.get("/")
def hello_index():
    return {"message": "Победа или смерть"}

# Run the FastAPI application with auto-reload enabled
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
