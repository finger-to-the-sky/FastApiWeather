import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
def welcome():
    return {'msg': 'Welcome to the FastAPI Weather!'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
