from django.contrib.auth.models import User
from django.contrib import admin
from .models import Product

import os
from dotenv import load_dotenv
load_dotenv()

adminName = os.environ.get("ADMIN_NAME")
adminEmail = os.environ.get("ADMIN_EMAIL")
adminPassword = os.environ.get("ADMIN_PASSWORD")

def create_superuser(username, email, password):
    if User.objects.filter(username=username).exists():
        print(f"Username {username} already exists.")
    else:
        User.objects.create_superuser(username, email, password)
        print(f"Superuser {username} created successfully.")

create_superuser(adminName, adminEmail, adminPassword)

admin.site.register(Product)