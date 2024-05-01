import uvicorn
from fastapi import FastAPI
from app.users.views import router as user_router

app = FastAPI()

app.include_router(user_router)


@app.get('/')
def welcome():
    return {'msg': 'Welcome to the FastAPI Weather!'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
