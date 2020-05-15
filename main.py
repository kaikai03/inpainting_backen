from typing import List
from fastapi import FastAPI, Path, Query, Header, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn as u
import time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/head")
async def read_items(*, user_agent: str = Header(None), x_token: List[str] = Header(None)):
    return {"User-Agent": user_agent}


@app.get("/headall/")
async def read_all(*, request: Request):
    return {"request.headers": request.headers}


@app.middleware("http")
async def my_middleware(request: Request, call_next):
    headers = request.headers
    print("middleware",headers)
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == '__main__':
    # --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
    u.run(app='main:app', host="127.0.0.1", port=9000, reload=True, debug=True)