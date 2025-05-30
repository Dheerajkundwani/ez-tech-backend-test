
from fastapi import FastAPI
from app import models, database
from app.users import router as user_router
from app.files import router as files_router

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(user_router)
app.include_router(files_router)
