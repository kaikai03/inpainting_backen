from typing import List
from fastapi import FastAPI, Path, Query, Header, Request
from starlette.middleware.cors import CORSMiddleware
import uvicorn as u
import time
from pydantic import BaseModel

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


@app.options("/")
async def options():
    return {"message": "options"}


@app.get("/")
async def root():
    return {"message": "Hello World"}


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


@app.post("/items/", response_model=Item)
async def create_item(item: Item):
    return item


if __name__ == '__main__':
    # --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
    u.run(app='main:app', host="127.0.0.1", port=9000, reload=True, debug=True)