import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from gada_chat_service.chat_service.router.channel_router import channel_router
from gada_chat_service.chat_service.router.user_router import user_router

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

app.router.prefix = "/api/v1"

app.include_router(user_router)
app.include_router(channel_router)

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8300)
