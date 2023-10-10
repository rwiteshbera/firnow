from fastapi import FastAPI

from routes import police_station

auth_service = FastAPI()
auth_service.include_router(police_station.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.auth:auth_service", port=8002)
