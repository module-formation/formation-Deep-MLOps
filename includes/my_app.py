from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Mathieu's API",
    description="Simple API to be define as a systemd service",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get(
    "/hello/",
    tags=["hello"],
    status_code=status.HTTP_200_OK,
    response_description="Hello !",
    summary="resume",
)
async def get_hello() -> str:
    return "Hello !"


if __name__ == "__main__":
    uvicorn.run(
        "my_app:app",
        host="127.0.0.1",
        port=8001,
        log_level="info",
        reload=True,
    )
