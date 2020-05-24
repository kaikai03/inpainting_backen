from typing import List
from fastapi import FastAPI, Path, Query, Header, Request, status, File, UploadFile, Form, HTTPException
# from fastapi.responses import HTMLResponse
from starlette.responses import HTMLResponse, JSONResponse


from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel

from fastapi import APIRouter
import app.constants as con


router = APIRouter()


class video_item(BaseModel):
    index: int = None
    name: str = None
    type: str = 0
    description: str = None
    cover: str
    src: str = None


@router.get("/random_final/{count}", response_model=List[video_item])
async def read_all(*, count: int):
    t = video_item(index=0, cover='http://127.0.0.1:90/imgs/1.jpg',src='http://127.0.0.1:90/v/1.mp4')
    t2 = video_item(index=1, cover='http://127.0.0.1:90/imgs/2.jpg',src='http://127.0.0.1:90/v/2.mp4')
    t3 = video_item(index=2, cover='http://127.0.0.1:90/imgs/3.gif', src='http://127.0.0.1:90/v/3.mp4')

    return [t,t2,t3]


@router.get("/random/{count}")
async def test(*, count: int):
    # test_ = [{"index":0,"type":"0","img":"http://127.0.0.1:90/imgs/1.jpg","media":"http://127.0.0.1:90/v/1.mp4"},
    #             {"index":1,"type":"1","img":"http://127.0.0.1:90/imgs/2.jpg","media":"http://127.0.0.1:90/v/2.mp4"},
    #             {"index":2,"type":"1","img":"http://127.0.0.1:90/imgs/3.gif","media":"http://127.0.0.1:90/v/3.mp4"}]
    # return test_
    t = video_item(index=0, cover='http://127.0.0.1:90/imgs/1.jpg', src='http://127.0.0.1:90/v/1.mp4')
    t2 = video_item(index=1, cover='http://127.0.0.1:90/imgs/2.jpg', src='http://127.0.0.1:90/v/2.mp4')
    t3 = video_item(index=2, cover='http://127.0.0.1:90/imgs/3.gif', src='http://127.0.0.1:90/v/3.mp4')
    return [t, t2, t3]

@router.get("/dbtest/")
async def init_db():
    con.global_db.history
    return "ok"




