import uvicorn
from fastapi import FastAPI

from services.location import location_service

app = FastAPI()

app.mount("/location", location_service)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True)
