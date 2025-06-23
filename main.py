import csv
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path

app = FastAPI()
BASE_DIR = Path(__file__).parent

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=BASE_DIR / "templates")

def read_csv_to_dicts(filename):
    filepath = BASE_DIR / "data" / filename  # <-- Шлях з "data"
    with open(filepath, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        return [row for row in reader]

@app.get("/")
async def read_root(request: Request):
    apps = read_csv_to_dicts("apps.csv")
    users = read_csv_to_dicts("users.csv")
    return templates.TemplateResponse("app_list.html", {"request": request, "apps": apps, "users": users})
