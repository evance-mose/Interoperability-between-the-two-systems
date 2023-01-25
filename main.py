from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import model
from database import engine, SessionLocal
from routers.mongodb import mongodbController
from routers.mysql import mysqlController

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(mongodbController.router, tags=['Patient'], prefix='/api/v1/patients')
app.include_router(mysqlController.router, tags=['Patient'], prefix='/api/v2/patients')



