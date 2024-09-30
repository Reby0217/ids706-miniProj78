import sqlite3

# Connect to the SQL database (create if not exists)
def connect_db():
    conn = sqlite3.connect("wealth_db.db")
    return conn


# Create the table
def create_table(conn):
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS wealthiest_people (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            country TEXT NOT NULL,
            industry TEXT NOT NULL,
            net_worth REAL NOT NULL,
            company TEXT NOT NULL
        )
    """
    )
    conn.commit()


# Insert records with manual IDs
def insert_data(conn):
    people = [
        (1, "Alice", "USA", "Tech", 100, "CompanyA"),
        (2, "Bob", "UK", "Finance", 200, "CompanyB"),
        (3, "Charlie", "Canada", "Tech", 150, "CompanyC"),
    ]
    cursor = conn.cursor()
    cursor.executemany(
        "INSERT INTO wealthiest_people (id, name, country, industry, net_worth, company) VALUES (?, ?, ?, ?, ?, ?)",
        people,
    )
    conn.commit()


# Retrieve all records, sorted by net worth
def retrieve_sorted_by_net_worth(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wealthiest_people ORDER BY net_worth DESC")
    rows = cursor.fetchall()
    print("Wealthiest People Records sorted by net worth:")
    for row in rows:
        print(row)


# Retrieve records filtered by industry (e.g., "Tech")
def retrieve_by_industry(conn, industry):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wealthiest_people WHERE industry = ?", (industry,))
    rows = cursor.fetchall()
    print(f"Wealthiest People Records in {industry} industry:")
    for row in rows:
        print(row)


# Update a record
def update_data(conn):
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE wealthiest_people SET net_worth = 180 WHERE name = 'Charlie'"
    )
    conn.commit()


# Delete a record
def delete_data(conn):
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wealthiest_people WHERE name = 'Bob'")
    conn.commit()


# Read records
def read_data(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wealthiest_people")
    rows = cursor.fetchall()
    print("Wealthiest People Records:")
    for row in rows:
        print(row)


def main():
    conn = connect_db()

    create_table(conn)
    insert_data(conn)
    read_data(conn)  # Check records
    retrieve_sorted_by_net_worth(conn)  # Retrieve sorted by net worth
    retrieve_by_industry(conn, "Tech")  # Retrieve only Tech industry
    update_data(conn)
    read_data(conn)  # Check update
    delete_data(conn)
    read_data(conn)  # Check delete
    conn.close()


if __name__ == "__main__":
    main()
