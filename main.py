import uvicorn
from asyncpg.exceptions import ForeignKeyViolationError
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from db import database, engine, SessionLocal
from routers import bookings, guests, payments, requests, rooms, users
from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from models import users as users_model
from models import bookings as bookings_model
from models import guests as guests_model
from models import requests as requests_model
from models import rooms as rooms_model
users_model.metadata.create_all(bind=engine)
guests_model.metadata.create_all(bind=engine)
rooms_model.metadata.create_all(bind=engine)
bookings_model.metadata.create_all(bind=engine)
requests_model.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


tags_metadata = [
    {   
        "name": "users",
    },
    {
        "name": "roomtypes",
    },
    {
        "name": "rooms",
    },
    {
        "name": "guests",
    },
    {
        "name": "bookings",
    },
    {
        "name": "requests",
    },
    {
        "name": "payments",
    },

]

# Initialize the app
app = FastAPI(title="StaySynergy", openapi_tags=tags_metadata, version="1.0.0",)


# Link all URLs
app.include_router(bookings.router)
app.include_router(guests.router)
app.include_router(payments.router)
app.include_router(requests.router)
app.include_router(rooms.router)
app.include_router(users.router)


@app.on_event('startup')
async def startup() -> None:
    await database.connect()


@app.on_event('shutdown')
async def shutdown() -> None:
    await database.disconnect()


@app.exception_handler(ForeignKeyViolationError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content={"message": str(exc)},
    )


if __name__ == '__main__':
    uvicorn.run("__main__:app", host="0.0.0.0", port=8888,
                reload=True, workers=2, debug=True)
