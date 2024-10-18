import argparse
import sqlite3


def count_words(filename):
    """
    Count words in a text file.
    input: filename (str)
    output: word_count (int)
    """
    with open(filename, "r") as file:
        text = file.read()
        words = text.split()
        return len(words)


def store_word_count(filename, word_count, conn):
    """
    Store the word count of a file in the given database connection.
    input: filename (str), word_count (int), conn (sqlite3.Connection)
    """
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS word_counts (
            filename TEXT PRIMARY KEY,
            word_count INTEGER
        )
    """
    )

    # Insert or update the word count for the file
    cursor.execute(
        """
        INSERT OR REPLACE INTO word_counts (filename, word_count)
        VALUES (?, ?)
    """,
        (filename, word_count),
    )

    conn.commit()


def main():
    conn = sqlite3.connect("word_counts.db")
    parser = argparse.ArgumentParser(description="Count words in a text file")
    parser.add_argument("filename", help="Path to the text file")
    args = parser.parse_args()
    word_count = count_words(args.filename)
    print(f"Word count: {word_count}")

    # Store the result in the database
    store_word_count(args.filename, word_count, conn)
    print(f"Word count for {args.filename} stored in the database.")
    conn.close()


if __name__ == "__main__":
    main()
