import pytest
from src.cli import (
    connect_db,
    create_table,
    insert_data,
    retrieve_sorted_by_net_worth,
    retrieve_by_industry,
    update_data,
    delete_data,
    read_data,
)


@pytest.fixture
def setup_database():
    conn = connect_db()
    create_table(conn)

    # Clear the table to avoid duplicate entries across test runs
    cursor = conn.cursor()
    cursor.execute("DELETE FROM wealthiest_people")
    conn.commit()  # Commit after clearing the table

    insert_data(conn)
    yield conn
    conn.close()  # Close the connection after the test


def test_create_table(setup_database):
    cursor = setup_database.cursor()
    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='wealthiest_people';"
    )
    result = cursor.fetchone()
    assert result is not None


def test_insert_data(setup_database):
    cursor = setup_database.cursor()
    cursor.execute("SELECT * FROM wealthiest_people")
    rows = cursor.fetchall()
    assert len(rows) == 3


def test_update_data(setup_database):
    update_data(setup_database)
    cursor = setup_database.cursor()
    cursor.execute("SELECT net_worth FROM wealthiest_people WHERE name = 'Charlie'")
    row = cursor.fetchone()
    assert row[0] == 180


def test_delete_data(setup_database):
    delete_data(setup_database)
    cursor = setup_database.cursor()
    cursor.execute("SELECT * FROM wealthiest_people WHERE name = 'Bob'")
    row = cursor.fetchone()
    assert row is None


def test_retrieve_sorted_by_net_worth(setup_database, capsys):
    # Capture the printed output of retrieve_sorted_by_net_worth function
    retrieve_sorted_by_net_worth(setup_database)
    captured = capsys.readouterr()

    # Split the output lines
    output_lines = captured.out.splitlines()

    # Verify the order of the output should be sorted by net worth in descending order
    assert "Wealthiest People Records sorted by net worth:" in output_lines[0]
    assert (
        "(2, 'Bob', 'UK', 'Finance', 200.0, 'CompanyB')" in output_lines[1]
    )  # Bob first
    assert (
        "(3, 'Charlie', 'Canada', 'Tech', 150.0, 'CompanyC')" in output_lines[2]
    )  # Charlie second
    assert (
        "(1, 'Alice', 'USA', 'Tech', 100.0, 'CompanyA')" in output_lines[3]
    )  # Alice third


def test_retrieve_by_industry(setup_database, capsys):
    # Capture the printed output of retrieve_by_industry function
    retrieve_by_industry(setup_database, "Tech")
    captured = capsys.readouterr()

    # Split the output lines
    output_lines = captured.out.splitlines()

    # Verify the first line contains the correct header
    assert "Wealthiest People Records in Tech industry:" in output_lines[0]

    # Verify the correct people are listed, in any order (Alice and Charlie)
    tech_records = [
        "(1, 'Alice', 'USA', 'Tech', 100.0, 'CompanyA')",
        "(3, 'Charlie', 'Canada', 'Tech', 150.0, 'CompanyC')",
    ]

    # Check that both records are present in the output
    assert any(tech_records[0] in line for line in output_lines)
    assert any(tech_records[1] in line for line in output_lines)

    # Exclude any lines that are not actual records (like summary log lines)
    tech_record_lines = [
        line for line in output_lines[1:] if "(" in line
    ]  # Skip the first line (header), and only count actual record lines

    # Verify that there are exactly two lines for "Tech" records
    assert len(tech_record_lines) == 2


def test_read_data(setup_database, capsys):
    # Capture the printed output of read_data function
    read_data(setup_database)
    captured = capsys.readouterr()

    # Verify expected output is in the captured output
    assert "Wealthiest People Records:" in captured.out
    assert "(1, 'Alice', 'USA', 'Tech', 100.0, 'CompanyA')" in captured.out
    assert "(2, 'Bob', 'UK', 'Finance', 200.0, 'CompanyB')" in captured.out
    assert "(3, 'Charlie', 'Canada', 'Tech', 150.0, 'CompanyC')" in captured.out
