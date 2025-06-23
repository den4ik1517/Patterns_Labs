import csv
import random
import os
from faker import Faker

fake = Faker()

num_records = 100

apps = []
users = []

for i in range(num_records):
    user = {
        "userId": f"user_{i+1}",
        "name": fake.name(),
        "email": fake.email(),
        "password": fake.password()
    }
    users.append(user)

for i in range(num_records):
    app = {
        "appId": f"app_{i+1}",
        "appName": fake.domain_word().capitalize() + "App",
        "description": fake.sentence(),
        "category": random.choice(["Games", "Productivity", "Health", "Education", "Entertainment"]),
        "version": f"{random.randint(1, 3)}.{random.randint(0, 9)}.{random.randint(0, 9)}",
        "size": round(random.uniform(5.0, 150.0), 2)
    }
    apps.append(app)

output_folder = r"C:\Users\dinis\patern\lab2\lab2_app_v2\data"
os.makedirs(output_folder, exist_ok=True)


user_file_path = os.path.join(output_folder, "users.csv")
app_file_path = os.path.join(output_folder, "apps.csv")

with open(user_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=users[0].keys())
    writer.writeheader()
    writer.writerows(users)

with open(app_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=apps[0].keys())
    writer.writeheader()
    writer.writerows(apps)

print(f"Файли збережено в папку '{output_folder}':\n- {user_file_path}\n- {app_file_path}")
print(f"\n✅ Файли збережено в папку '{output_folder}':")
print(f"- {user_file_path}")
print(f"- {app_file_path}")
