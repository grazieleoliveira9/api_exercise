from fastapi import FastAPI
from app.routers.users import router as users_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(users_router, prefix="/api/v1")





