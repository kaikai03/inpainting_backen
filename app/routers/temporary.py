from fastapi import FastAPI, Path, Query, Header, Request, status, File, UploadFile, Form, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse, JSONResponse
from fastapi.exception_handlers import ( http_exception_handler, request_validation_exception_handler, )
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi import Depends
from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel


from typing import List
from fastapi import FastAPI, Path, Query, Header, Request, status, File, UploadFile, Form, HTTPException
# from fastapi.responses import HTMLResponse
from starlette.responses import HTMLResponse, JSONResponse


from fastapi.encoders import jsonable_encoder

from pydantic import BaseModel

from fastapi import APIRouter
import app.constants as con


router = APIRouter()

@router.options("/")
async def options():
    return {"message": "options"}


@router.get("/", status_code=status.HTTP_200_OK)
async def root():
    print(con.db.base)
    # 使用Response包装时，将无视装饰器中的status
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Hello World"})


@router.post("/p")
async def root():
    return {"message": "p"}


@router.get("/head")
async def read_items(*, user_agent: str = Header(None), x_token: List[str] = Header(None)):
    return {"User-Agent": user_agent}


@router.get("/headall/")
async def read_all(*, request: Request):
    return {"request.headers": request.headers}


class Item(BaseModel):
    name: str
    description: str = None
    price: float = 999
    tax: float = None
    tags: List[str] = []


fake_db = {}


@router.post("/items/", response_model=Item)
async def create_item(item: Item):
    if item is None:
        raise HTTPException(status_code=405, detail="Item not found", headers={"X-Error": "There goes my error"})
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return item


@router.get("/index_x")
async def main():
    content = """
            <body>
            <form action="/files/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <input type="submit">
            </form>
            <form action="/uploadfiles/" enctype="multipart/form-data" method="post">
            <input name="files" type="file" multiple>
            <input type="submit">
            </form>
            <form action="/files3/" enctype="multipart/form-data" method="post">
            <input name="file" type="file">
            <input name="fileb" type="file">
            <input name="token" type="text">
            <input type="submit">
            </form>
            </body>
             """
    return HTMLResponse(content=content)


@router.post("/files_x/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@router.post("/uploadfiles_x/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    # filename  content_type  file   await{write(data), read(size), seek(offset), close()}
    return {"filenames": [file.filename for file in files]}


@router.post("/files3_x/")
async def create_file(
 file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }

