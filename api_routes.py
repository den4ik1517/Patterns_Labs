from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse
from .database import (
    get_connection,
    insert_app,  # функція для вставки даних для додатків
    insert_user,  # функція для вставки даних для користувачів  
)
from .models import AppCreate, UserCreate  # Створимо нові моделі для App і User
from .upload_csv import process_uploaded_csv

router = APIRouter()

# Отримати всі додатки
@router.get("/apps")
def get_all_apps():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Apps")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Отримати один додаток
@router.get("/apps/{app_id}")
def get_app(app_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Apps WHERE appId=%s", (app_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        return JSONResponse(status_code=404, content={"detail": f"App with ID {app_id} not found"})
    return result

# Створити додаток
@router.post("/apps")
def create_app(app: AppCreate):
    insert_app(app.dict())  # Передаємо словник даних в функцію
    return {"message": "App added or updated"}

# Оновити додаток
@router.put("/apps/{app_id}")
def update_app(app_id: str, app: AppCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT appId FROM Apps WHERE appId=%s", (app_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return JSONResponse(status_code=404, content={"detail": f"App with ID {app_id} not found"})
    cursor.execute("""
        UPDATE Apps
        SET appName=%s, description=%s, category=%s, version=%s, size=%s
        WHERE appId=%s
    """, (app.appName, app.description, app.category, app.version, app.size, app_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "App updated"}

# Видалити додаток
@router.delete("/apps/{app_id}")
def delete_app(app_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Apps WHERE appId=%s", (app_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "App deleted"}

# Отримати всіх користувачів
@router.get("/users")
def get_all_users():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users")
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

# Отримати одного користувача
@router.get("/users/{user_id}")
def get_user(user_id: str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Users WHERE userId=%s", (user_id,))
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    if not result:
        return JSONResponse(status_code=404, content={"detail": f"User with ID {user_id} not found"})
    return result

# Створити користувача
@router.post("/users")
def create_user(user: UserCreate):
    insert_user(user.dict())  # Передаємо словник даних в функцію
    return {"message": "User added or updated"}

# Оновити користувача
@router.put("/users/{user_id}")
def update_user(user_id: str, user: UserCreate):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT userId FROM Users WHERE userId=%s", (user_id,))
    if cursor.fetchone() is None:
        cursor.close()
        conn.close()
        return JSONResponse(status_code=404, content={"detail": f"User with ID {user_id} not found"})
    cursor.execute("""
        UPDATE Users
        SET name=%s, email=%s, password=%s
        WHERE userId=%s
    """, (user.name, user.email, user.password, user_id))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User updated"}

# Видалити користувача
@router.delete("/users/{user_id}")
def delete_user(user_id: str):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Users WHERE userId=%s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()
    return {"message": "User deleted"}

# Завантажити і обробити CSV
@router.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    if not file.filename.endswith(".csv"):
        return JSONResponse(status_code=400, content={"detail": "Only CSV files are allowed"})
    await process_uploaded_csv(file)  # Це має обробляти додатки та користувачів
    return {"message": "CSV uploaded and processed successfully"}
