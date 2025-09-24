from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import chat, upload_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # in dev, later restrict to frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(chat.router)
app.include_router(upload_data.router)