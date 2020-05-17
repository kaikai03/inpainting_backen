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

import uvicorn as u
import time
from pydantic import BaseModel

from tinydb import TinyDB, Query
# db = TinyDB('./db.json')
# db.insert({'int': 1, 'char': 'a'})
# db.insert({'int': 1, 'char': 'b'})

app = FastAPI()

# request need "Origin"
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    max_age=999
)

@app.middleware("http")
async def my_middleware(request: Request, call_next):
    headers = request.headers
    print("middleware",headers)
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"OMG! An HTTP error!: {exc}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f"OMG! The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

# raise HTTPException(status_code=418, detail="Nope! I don't like 3.")


@app.options("/")
async def options():
    return {"message": "options"}


@app.get("/", status_code=status.HTTP_200_OK)
async def root():
    # 使用Response包装时，将无视装饰器中的status
    return JSONResponse(status_code=status.HTTP_202_ACCEPTED, content={"message": "Hello World"})


@app.post("/p")
async def root():
    return {"message": "p"}


@app.get("/head")
async def read_items(*, user_agent: str = Header(None), x_token: List[str] = Header(None)):
    return {"User-Agent": user_agent}


@app.get("/headall/")
async def read_all(*, request: Request):
    return {"request.headers": request.headers}





class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None
    tags: List[str] = []

fake_db = {}
@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    if item is None:
        raise HTTPException(status_code=405, detail="Item not found", headers={"X-Error": "There goes my error"})
    json_compatible_item_data = jsonable_encoder(item)
    fake_db[id] = json_compatible_item_data
    return item


@app.get("/index")
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


@app.post("/files/")
async def create_files(files: List[bytes] = File(...)):
    return {"file_sizes": [len(file) for file in files]}


@app.post("/uploadfiles/")
async def create_upload_files(files: List[UploadFile] = File(...)):
    # filename  content_type  file   await{write(data), read(size), seek(offset), close()}
    return {"filenames": [file.filename for file in files]}


@app.post("/files3/")
async def create_file(
 file: bytes = File(...), fileb: UploadFile = File(...), token: str = Form(...)):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


if __name__ == '__main__':
    # --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
    u.run(app='main:app', host="127.0.0.1", port=9000, reload=True, debug=True)