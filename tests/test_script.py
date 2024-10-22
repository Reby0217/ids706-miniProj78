import os
import pytest
import sqlite3
from word_counter_py.cli import count_words, store_word_count


@pytest.fixture(scope="session")
def db_connection():
    """Create and return a database connection that is shared across the test session."""
    conn = sqlite3.connect(":memory:")  # Use an in-memory SQLite database for testing
    cursor = conn.cursor()

    # Create the `word_counts` table
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS word_counts (
            filename TEXT PRIMARY KEY,
            word_count INTEGER
        )
    """
    )
    conn.commit()
    yield conn
    conn.close()


@pytest.fixture(autouse=True)
def setup_transaction(db_connection):
    """Automatically start a transaction and rollback after each test."""
    cursor = db_connection.cursor()
    cursor.execute("BEGIN;")
    yield
    db_connection.rollback()


def test_count_words():
    """Test the word counting functionality."""
    # Create a temporary test file
    test_file = "test_file.txt"
    with open(test_file, "w") as file:
        file.write("This is a sample test file with some words.")

    # Count the words in the file
    word_count = count_words(test_file)
    assert word_count == 9  # Expecting 9 words

    # Clean up the test file
    os.remove(test_file)


def test_store_word_count(db_connection):
    """Test storing the word count in the database."""
    cursor = db_connection.cursor()

    # Store a word count for a file
    test_file = "test_file.txt"
    word_count = 8
    store_word_count(test_file, word_count, db_connection)

    # Query the database to check if the word count was stored
    cursor.execute(
        "SELECT word_count FROM word_counts WHERE filename = ?", (test_file,)
    )
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == word_count


def test_empty_file(db_connection):
    """Test counting words in an empty file and storing the result."""
    # Create an empty test file
    test_file = "empty_file.txt"
    with open(test_file, "w"):
        pass  # Create an empty file

    # Count the words in the file
    word_count = count_words(test_file)
    assert word_count == 0  # Expecting 0 words in an empty file

    # Store the word count in the database
    store_word_count(test_file, word_count, db_connection)

    # Query the database to check if the word count was stored
    cursor = db_connection.cursor()
    cursor.execute(
        "SELECT word_count FROM word_counts WHERE filename = ?", (test_file,)
    )
    result = cursor.fetchone()
    assert result is not None
    assert result[0] == word_count

    # Clean up the test file
    os.remove(test_file)


def test_nonexistent_file():
    """Test when the input file does not exist."""
    nonexistent_file = "nonexistent_file.txt"
    with pytest.raises(FileNotFoundError):
        count_words(nonexistent_file)  # Expecting a FileNotFoundError
