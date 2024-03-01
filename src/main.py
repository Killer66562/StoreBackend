import uvicorn

from fastapi import FastAPI

from routes import city, district


app = FastAPI()
app.include_router(city.router)
app.include_router(district.router)

@app.get("/")
def hello():
    return {"message": "Hello, world!"}

if __name__ == '__main__':
    uvicorn.run("main:app", reload=True)