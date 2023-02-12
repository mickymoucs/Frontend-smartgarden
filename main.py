from fastapi import FastAPI
from routers import garden, update
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(garden.router)
app.include_router(update.router)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "Welcome to my little garden."}
