import pytest
import mysql.connector
from src.cli import init, complex_query


@pytest.fixture
def setup_database():
    # Connect to the MySQL database
    conn = mysql.connector.connect(
        host="localhost", user="root", password="qwer1234", database="ecommerce_db"
    )

    # Create the tables and insert the initial data
    init()

    yield conn

    # Clean up the database after each test
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS customers")
    conn.commit()
    conn.close()


def test_create_tables(setup_database):
    cursor = setup_database.cursor()
    # Check if the `customers` table exists
    cursor.execute("SHOW TABLES LIKE 'customers'")
    result = cursor.fetchone()
    assert result is not None

    # Check if the `products` table exists
    cursor.execute("SHOW TABLES LIKE 'products'")
    result = cursor.fetchone()
    assert result is not None

    # Check if the `orders` table exists
    cursor.execute("SHOW TABLES LIKE 'orders'")
    result = cursor.fetchone()
    assert result is not None


def test_insert_data(setup_database):
    cursor = setup_database.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    assert len(customers) == 2  # John Doe and Jane Smith

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    assert len(products) == 3  # Laptop, Headphones, Keyboard

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    assert len(orders) == 3  # Orders from the sample data


def test_complex_query(setup_database, capsys):
    # Capture the output of the complex query function
    complex_query()
    captured = capsys.readouterr()

    # Check the output contains expected values
    assert "Customer: John Doe" in captured.out
    assert "Total Orders: 2" in captured.out
    assert "Total Spent: $1399.97" in captured.out
    assert "Customer: Jane Smith" in captured.out
    assert "Total Orders: 1" in captured.out
    assert "Total Spent: $49.99" in captured.out
