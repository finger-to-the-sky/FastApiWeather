import uvicorn
from fastapi import FastAPI
from app.users.views import router as user_router
from app.auth.views import router as auth_router
from app.users.management.users import router as manage_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(manage_router)

@app.get('/')
def welcome():
    return {'msg': 'Welcome to the FastAPI Weather!'}


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
