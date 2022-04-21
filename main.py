import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gada_chat_service.chat_service.router.v1.channel_router import channel_router
from gada_chat_service.chat_service.router.v1.user_router import user_router
from gada_chat_service.chat_service.router.v1.v1 import v1_router

app = FastAPI()

origins = [
    "http://localhost",
    "https://localhost",
    "http://localhost:3000",
    "https://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.router.prefix = "/api"

app.include_router(v1_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8300)
