from fastapi import UploadFile
from .database import insert_user, insert_app, get_connection
import csv
from io import StringIO

async def process_uploaded_csv(file: UploadFile):
    """
    Читає один CSV-файл:
      - якщо в заголовку є 'userId' — очищає Users і вставляє всіх користувачів
      - elif є 'appId' — очищає Apps і вставляє всі додатки
    """

    content = await file.read()
    text = content.decode('utf-8')
    reader = csv.DictReader(StringIO(text))
    fields = reader.fieldnames or []

    if 'userId' in fields:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Users")
        cur.execute("ALTER TABLE Users AUTO_INCREMENT = 1")
        conn.commit()
        cur.close()
        conn.close()

        for row in reader:
            if row.get('userId') and row.get('name') and row.get('email') and row.get('password'):
                insert_user({
                    'userId': row['userId'],
                    'name': row['name'],
                    'email': row['email'],
                    'password': row['password']
                })

    elif 'appId' in fields:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Apps")
        cur.execute("ALTER TABLE Apps AUTO_INCREMENT = 1")
        conn.commit()
        cur.close()
        conn.close()

        for row in reader:
            if all(row.get(k) for k in ('appId','appName','description','category','version','size')):
                insert_app({
                    'appId': row['appId'],
                    'appName': row['appName'],
                    'description': row['description'],
                    'category': row['category'],
                    'version': row['version'],
                    'size': float(row['size'])
                })

    else:
        raise ValueError("CSV file must contain either 'userId' or 'appId' column")
