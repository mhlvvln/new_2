import asyncio

from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse

#from database.database import init_models
from models import File
from router import router as files_router

app = FastAPI(title="FileServer e-notGPT",
              description="Файловый сервер для фотографий[2МБ], видео[100МБ], документов[50МБ]")
app.include_router(files_router, tags=["Files"])

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(HTTPException)
async def unicorn_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"status": False, "error": exc.detail},
    )
