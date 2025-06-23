from fastapi import APIRouter, Request, Form, UploadFile, File, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from ..database import get_connection, insert_app, insert_user
from ..upload_csv import process_uploaded_csv
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter()

@router.get("/apps")
def list_apps(request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Apps")
    apps = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("app_list.html", {"request": request, "apps": apps})

@router.get("/apps/add")
def add_app_form(request: Request):
    return templates.TemplateResponse("app_form.html", {"request": request, "action": "Add", "app": {}})

@router.post("/apps/add")
def add_app(name: str = Form(...), description: str = Form(...)):
    insert_app(name, description)
    return RedirectResponse(url="/apps", status_code=303)

@router.get("/apps/edit/{app_id}")
def edit_app_form(app_id: int, request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Apps WHERE id=%s", (app_id,))
    app = cursor.fetchone()
    cursor.close()
    conn.close()
    if not app:
        raise HTTPException(status_code=404, detail="App not found")
    return templates.TemplateResponse("app_form.html", {"request": request, "action": "Edit", "app": app})

@router.post("/apps/edit/{app_id}")
def edit_app(app_id: int, name: str = Form(...), description: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Apps WHERE id=%s", (app_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="App not found for editing")
    cursor.execute("UPDATE Apps SET name=%s, description=%s WHERE id=%s", (name, description, app_id))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/apps", status_code=303)

@router.get("/apps/delete/{app_id}")
def delete_app(app_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Apps WHERE id=%s", (app_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="App was already removed")
    cursor.execute("DELETE FROM Apps WHERE id=%s", (app_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/apps", status_code=303)

@router.get("/users")
def list_users(request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

@router.get("/users/add")
def add_user_form(request: Request):
    return templates.TemplateResponse("user_form.html", {"request": request, "action": "Add", "user": {}})

@router.post("/users/add")
def add_user(username: str = Form(...), email: str = Form(...)):
    insert_user(username, email)
    return RedirectResponse(url="/users", status_code=303)

@router.get("/users/edit/{user_id}")
def edit_user_form(user_id: int, request: Request):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE id=%s", (user_id,))
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return templates.TemplateResponse("user_form.html", {"request": request, "action": "Edit", "user": user})

@router.post("/users/edit/{user_id}")
def edit_user(user_id: int, username: str = Form(...), email: str = Form(...)):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE id=%s", (user_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User not found for editing")
    cursor.execute("UPDATE Users SET username=%s, email=%s WHERE id=%s", (username, email, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/users", status_code=303)

@router.get("/users/delete/{user_id}")
def delete_user(user_id: int):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM Users WHERE id=%s", (user_id,))
    existing = cursor.fetchone()
    if not existing:
        cursor.close()
        conn.close()
        raise HTTPException(status_code=404, detail="User was already removed")
    cursor.execute("DELETE FROM Users WHERE id=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return RedirectResponse(url="/users", status_code=303)

@router.get("/upload-csv")
def upload_csv_form(request: Request):
    return templates.TemplateResponse("upload_csv.html", {"request": request})

@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    await process_uploaded_csv(file)
    return RedirectResponse(url="/apps", status_code=303)
