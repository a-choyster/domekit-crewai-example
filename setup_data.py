"""Create sample product database for the CrewAI + DomeKit example."""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "products.db")


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            price REAL NOT NULL,
            units_sold INTEGER NOT NULL,
            revenue REAL NOT NULL
        )
    """)

    products = [
        ("Wireless Headphones", "Electronics", 79.99, 1200, 95988.00),
        ("Ergonomic Keyboard", "Electronics", 129.99, 850, 110491.50),
        ("Standing Desk", "Furniture", 499.99, 320, 159996.80),
        ("Laptop Stand", "Accessories", 39.99, 2100, 83979.00),
        ("USB-C Hub", "Electronics", 54.99, 1800, 98982.00),
        ("Monitor Light Bar", "Accessories", 44.99, 950, 42740.50),
        ("Mechanical Pencil Set", "Stationery", 12.99, 3200, 41568.00),
        ("Desk Organizer", "Accessories", 29.99, 1400, 41986.00),
        ("Webcam HD", "Electronics", 89.99, 720, 64792.80),
        ("Noise Machine", "Wellness", 34.99, 600, 20994.00),
        ("Desk Plant Kit", "Wellness", 24.99, 900, 22491.00),
        ("Cable Management Kit", "Accessories", 19.99, 2500, 49975.00),
        ("Task Chair", "Furniture", 349.99, 410, 143495.90),
        ("Whiteboard", "Stationery", 59.99, 500, 29995.00),
        ("Portable Charger", "Electronics", 44.99, 1600, 71984.00),
    ]

    cur.executemany(
        "INSERT INTO products (name, category, price, units_sold, revenue) VALUES (?, ?, ?, ?, ?)",
        products,
    )

    conn.commit()
    conn.close()

    print(f"Created {DB_PATH} with {len(products)} products.")


if __name__ == "__main__":
    main()
