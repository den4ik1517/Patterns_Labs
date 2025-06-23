import csv
from fastapi import UploadFile
from .database import insert_app, insert_user

async def process_uploaded_csv(file: UploadFile):
    contents = await file.read()
    decoded = contents.decode("utf-8").splitlines()
    reader = csv.DictReader(decoded)


    headers = reader.fieldnames

    if not headers:
        raise ValueError("Empty CSV file or invalid format")


    app_columns = {"appId", "appName", "description", "category", "version", "size"}
    user_columns = {"userId", "name", "email", "password"}

    if app_columns.issubset(set(headers)):
        for row in reader:
            try:
                row["size"] = float(row["size"])
            except (ValueError, KeyError):
                row["size"] = 0.0
            insert_app(row)
    elif user_columns.issubset(set(headers)):
        for row in reader:
            insert_user(row)
    else:
        raise ValueError("CSV headers do not match Apps or Users format")
