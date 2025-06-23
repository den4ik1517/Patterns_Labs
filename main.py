from fastapi import FastAPI, UploadFile
from .upload_csv import process_uploaded_csv
from .api_routes import router
from .database import init_db
from .exceptions import (
    custom_http_exception_handler,
    validation_exception_handler,
    generic_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
from contextlib import asynccontextmanager
from pathlib import Path

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()

    base_dir = Path(__file__).parent.parent / 'data'

    users_path = base_dir / 'users.csv'
    if users_path.exists():
        upload_file = UploadFile(filename='users.csv', file=users_path.open('rb'))
        await process_uploaded_csv(upload_file)
        upload_file.file.close()

    apps_path = base_dir / 'apps.csv'
    if apps_path.exists():
        upload_file = UploadFile(filename='apps.csv', file=apps_path.open('rb'))
        await process_uploaded_csv(upload_file)
        upload_file.file.close()

    yield

app = FastAPI(lifespan=lifespan)

app.add_exception_handler(StarletteHTTPException, custom_http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)

app.include_router(router)
