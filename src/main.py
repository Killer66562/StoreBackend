import uvicorn

from fastapi import FastAPI


app = FastAPI()

@app.get("/")
def hello():
    return {"message": "Hello, world!"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)