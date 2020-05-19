from typing import List
from fastapi import FastAPI, Path, Query, Header, Request, status, File, UploadFile, Form, HTTPException
# from fastapi.responses import HTMLResponse
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.exception_handlers import ( http_exception_handler, request_validation_exception_handler, )
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel

from fastapi import Depends
from fastapi import APIRouter
import app.global_db as db



router = APIRouter()


@router.get("/", tags=["users"])
def read_users():
    return [{"username": "sub"}, {"username": "Bar"}]


@router.get("/me", tags=["users"])
async def read_user_me():
    return {"username": "fakecurrentuser"}


@router.get("/{username}", tags=["users"])
async def read_user(username: str):
    return {"username": username}