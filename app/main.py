from fastapi import FastAPI, Depends, Header, Request, HTTPException
from starlette.middleware.cors import CORSMiddleware
from fastapi.exception_handlers import ( http_exception_handler, request_validation_exception_handler, )
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException


import uvicorn as u
import time

from app.routers import root
from app.routers import user
import app.constants as con

from app.routers import temporary

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


async def get_token_header(x_token: str = Header(None)):
    if x_token is not None:
        raise HTTPException(status_code=400, detail="X-Token header invalid")
    return "main"

app.include_router(
    root.router,
    tags=["root"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    user.router,
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)

app.include_router(
    user.router,
    prefix="/test",
    tags=["test"],
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    print(f"An HTTP error!: {exc}")
    return await http_exception_handler(request, exc)


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    print(f" The client sent invalid data!: {exc}")
    return await request_validation_exception_handler(request, exc)

# raise HTTPException(status_code=418, detail="Nope! I don't like 3.")




if __name__ == '__main__':
    # --ssl-keyfile=./key.pem --ssl-certfile=./cert.pem
    u.run(app='main:app', host="127.0.0.1", port=9000, reload=True, debug=True)