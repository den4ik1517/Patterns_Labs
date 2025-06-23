import mysql.connector
from mysql.connector import MySQLConnection

DB_CONFIG = {
    "user": "root",
    "password": "DanYliukDenys1234____&&/.,mdgh",
    "host": "localhost",
    "database": "patern_data",
}

def get_connection() -> MySQLConnection:
    return mysql.connector.connect(**DB_CONFIG)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                userId VARCHAR(50) UNIQUE,
                name VARCHAR(255),
                email VARCHAR(255),
                password VARCHAR(255)
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Apps (
                id INT AUTO_INCREMENT PRIMARY KEY,
                appId VARCHAR(50) UNIQUE,
                appName VARCHAR(255),
                description TEXT,
                category VARCHAR(100),
                version VARCHAR(20),
                size DOUBLE
            );
        """)
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def insert_user(user_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Users (userId, name, email, password)
            VALUES (%s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name=VALUES(name),
                email=VALUES(email),
                password=VALUES(password)
        """, (
            user_data['userId'],
            user_data['name'],
            user_data['email'],
            user_data['password'],
        ))
        conn.commit()
    finally:
        cursor.close()
        conn.close()

def insert_app(app_data: dict):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            INSERT INTO Apps (appId, appName, description, category, version, size)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                appName=VALUES(appName),
                description=VALUES(description),
                category=VALUES(category),
                version=VALUES(version),
                size=VALUES(size)
        """, (
            app_data['appId'],
            app_data['appName'],
            app_data['description'],
            app_data['category'],
            app_data['version'],
            app_data['size'],
        ))
        conn.commit()
    finally:
        cursor.close()
        conn.close()
