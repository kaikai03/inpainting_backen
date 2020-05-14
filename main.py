from fastapi import FastAPI
import uvicorn as u

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == '__main__':
    u.run(app)