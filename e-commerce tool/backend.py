from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
import requests
import jwt
import datetime
import os
import sqlite3

app = FastAPI()

# Database Connection
DB_NAME = "ecommerce.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            email TEXT PRIMARY KEY,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL,
            stock INTEGER
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_email TEXT,
            product_id INTEGER,
            quantity INTEGER,
            FOREIGN KEY(user_email) REFERENCES users(email),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)
    conn.commit()
    conn.close()

init_db()

# Authentication Config (Use a secure secret key in production)
SECRET_KEY = "your_secret_key"

# User Model
class User(BaseModel):
    email: str
    password: str

# Token Generation
def create_jwt_token(user_email):
    expiration = datetime.datetime.utcnow() + datetime.timedelta(days=7)
    token = jwt.encode({"sub": user_email, "exp": expiration}, SECRET_KEY, algorithm="HS256")
    return token

# User Registration
@app.post("/register")
def register_user(user: User):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE email = ?", (user.email,))
    if cursor.fetchone():
        conn.close()
        raise HTTPException(status_code=400, detail="User already exists")
    cursor.execute("INSERT INTO users (email, password) VALUES (?, ?)", (user.email, user.password))
    conn.commit()
    conn.close()
    return {"message": "User registered successfully"}

# User Login
@app.post("/login")
def login_user(user: User):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE email = ?", (user.email,))
    result = cursor.fetchone()
    conn.close()
    if not result or result[0] != user.password:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = create_jwt_token(user.email)
    return {"access_token": token}

# Fetch Dashboard Data
@app.get("/dashboard")
def get_dashboard_data():
    return {
        "overview": {
            "total_sales": "$50,000",
            "total_orders": 1200,
            "conversion_rate": "3%",
            "average_order_value": "$42"
        },
        "automation_performance": {
            "tasks_automated": 300,
            "time_saved": "500 hours",
            "automation_rate": "90%",
            "error_rate": "1%"
        },
        "order_management": {
            "new_orders": 50,
            "shipped_orders": 1100,
            "cancelled_orders": 30,
            "order_status_chart": "chart_data"
        },
        "inventory_management": {
            "low_stock_items": 5,
            "out_of_stock_items": 2,
            "inventory_value": "$200,000",
            "inventory_levels_chart": "chart_data"
        },
        "customer_management": {
            "new_customers": 120,
            "returning_customers": 80,
            "customer_satisfaction": "8.5/10",
            "customer_segments_chart": "chart_data"
        },
        "analytics": {
            "sales_by_channel_chart": "chart_data",
            "sales_by_product_chart": "chart_data",
            "sales_by_region_chart": "chart_data"
        },
        "alerts": [
            "Low Stock Alert: Item XYZ is running low",
            "Order Error Alert: Order #123 failed to ship",
            "System Update Alert: New version available for download"
        ],
        "quick_actions": [
            "Run Automation Task: Run task XYZ",
            "View Order Details: View order #123",
            "Manage Inventory: Manage inventory levels"
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
