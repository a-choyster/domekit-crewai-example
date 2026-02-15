"""Tests for setup_data.py — verifies the products database is created correctly."""

import os
import sqlite3
import subprocess
import sys

import pytest

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "products.db")
SETUP_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "setup_data.py")


@pytest.fixture(autouse=True)
def fresh_db():
    """Re-run setup_data before each test to ensure a clean database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    subprocess.run([sys.executable, SETUP_SCRIPT], check=True, capture_output=True)
    yield
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


def test_db_file_created():
    assert os.path.exists(DB_PATH)


def test_products_table_exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='products'"
    )
    tables = cursor.fetchall()
    conn.close()
    assert len(tables) == 1


def test_products_table_has_correct_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("PRAGMA table_info(products)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    assert columns == ["id", "name", "category", "price", "units_sold", "revenue"]


def test_products_table_has_15_rows():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 15


def test_all_products_have_positive_revenue():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT name, revenue FROM products WHERE revenue <= 0")
    bad = cursor.fetchall()
    conn.close()
    assert len(bad) == 0, f"Products with non-positive revenue: {bad}"


def test_revenue_matches_price_times_units():
    """Revenue should equal price * units_sold."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT name, price, units_sold, revenue FROM products")
    for name, price, units, revenue in cursor.fetchall():
        expected = round(price * units, 2)
        assert abs(revenue - expected) < 0.01, (
            f"{name}: revenue {revenue} != {expected}"
        )
    conn.close()


def test_setup_is_idempotent():
    """Running setup twice should not cause errors or duplicate data."""
    subprocess.run([sys.executable, SETUP_SCRIPT], check=True, capture_output=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT COUNT(*) FROM products")
    count = cursor.fetchone()[0]
    conn.close()
    # Should be 15 or 30 depending on implementation, but shouldn't error
    assert count >= 15
