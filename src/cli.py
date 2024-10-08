import mysql.connector

# Create a connection to the MySQL server
connection = mysql.connector.connect(host="localhost", user="root", password="qwer1234")

# Create a cursor to execute SQL queries
cursor = connection.cursor()

# Create a new database if it doesn't already exist
cursor.execute("CREATE DATABASE IF NOT EXISTS ecommerce_db")

# Close the cursor and the initial connection
cursor.close()
connection.close()

# Create a connection to the MySQL database
connection = mysql.connector.connect(
    host="localhost", user="root", password="qwer1234", database="ecommerce_db"
)

# Create a cursor to execute SQL queries
cursor = connection.cursor()


def init():
    """Initialize the project by creating or clearing tables."""
    # Clear or create the customers table
    cursor.execute("DROP TABLE IF EXISTS orders")
    cursor.execute("DROP TABLE IF EXISTS products")
    cursor.execute("DROP TABLE IF EXISTS customers")

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_name VARCHAR(255) NOT NULL,
            customer_email VARCHAR(255) NOT NULL UNIQUE
        )
        """
    )

    # Clear or create the products table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT AUTO_INCREMENT PRIMARY KEY,
            product_name VARCHAR(255) NOT NULL,
            price DECIMAL(10, 2) NOT NULL
        )
        """
    )

    # Clear or create the orders table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id INT AUTO_INCREMENT PRIMARY KEY,
            customer_id INT,
            product_id INT,
            quantity INT NOT NULL,
            order_date DATE,
            FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
            FOREIGN KEY (product_id) REFERENCES products(product_id)
        )
        """
    )

    # Insert sample data into customers table
    cursor.execute(
        "INSERT INTO customers (customer_name, customer_email) VALUES ('John Doe', 'john@example.com')"
    )
    cursor.execute(
        "INSERT INTO customers (customer_name, customer_email) VALUES ('Jane Smith', 'jane@example.com')"
    )

    # Insert sample data into products table
    cursor.execute(
        "INSERT INTO products (product_name, price) VALUES ('Laptop', 999.99)"
    )
    cursor.execute(
        "INSERT INTO products (product_name, price) VALUES ('Headphones', 199.99)"
    )
    cursor.execute(
        "INSERT INTO products (product_name, price) VALUES ('Keyboard', 49.99)"
    )

    # Insert sample data into orders table
    cursor.execute(
        "INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (1, 1, 1, '2023-09-15')"
    )
    cursor.execute(
        "INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (1, 2, 2, '2023-09-16')"
    )
    cursor.execute(
        "INSERT INTO orders (customer_id, product_id, quantity, order_date) VALUES (2, 3, 1, '2023-09-17')"
    )

    # Commit the changes
    connection.commit()
    print("Tables created/cleared and sample data inserted successfully.")


def complex_query():
    """A complex query to fetch customer details and their order history with aggregation."""
    sql_query = """
    SELECT
        customers.customer_name,
        customers.customer_email,
        COUNT(orders.order_id) AS total_orders,
        COALESCE(SUM(orders.quantity * products.price), 0) AS total_spent,
        MAX(orders.order_date) AS last_order_date
    FROM
        customers
    LEFT JOIN
        orders ON customers.customer_id = orders.customer_id
    LEFT JOIN
        products ON orders.product_id = products.product_id
    GROUP BY
        customers.customer_id
    ORDER BY
        total_spent DESC;
    """

    # Execute the SQL query
    cursor.execute(sql_query)

    # Fetch all the results
    results = cursor.fetchall()

    # Process and print the results
    for row in results:
        customer_name, customer_email, total_orders, total_spent, last_order_date = row
        print(f"Customer: {customer_name} ({customer_email})")
        print(f"Total Orders: {total_orders}")
        print(f"Total Spent: ${total_spent:.2f}")
        print(f"Last Order Date: {last_order_date}")
        print()


def main():
    init()
    complex_query()


if __name__ == "__main__":
    main()
