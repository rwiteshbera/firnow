from fastapi import FastAPI

from routes import police

auth_service = FastAPI()
auth_service.include_router(police.router)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("services.auth:auth_service", port=8002)
