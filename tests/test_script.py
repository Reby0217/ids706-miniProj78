import pytest
import mysql.connector
from src.cli import init, complex_query


@pytest.fixture(scope="session")
def db_connection():
    """Create and return a database connection that is shared across the test session."""
    conn = mysql.connector.connect(
        host="localhost", user="root", password="qwer1234", database="ecommerce_db"
    )

    # Ensure the tables are created only once for all tests
    init()  # Assuming `init` creates and populates tables
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def setup_transaction(db_connection):
    """Automatically start a transaction and rollback after each test to avoid re-creating tables."""
    cursor = db_connection.cursor()
    cursor.execute("START TRANSACTION;")
    yield
    db_connection.rollback()


def test_create_tables(db_connection):
    cursor = db_connection.cursor()

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


def test_insert_data(db_connection):
    cursor = db_connection.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    assert len(customers) == 2  # John Doe and Jane Smith

    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    assert len(products) == 3  # Laptop, Headphones, Keyboard

    cursor.execute("SELECT * FROM orders")
    orders = cursor.fetchall()
    assert len(orders) == 3  # Orders from the sample data


def test_complex_query(db_connection, capsys):
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
