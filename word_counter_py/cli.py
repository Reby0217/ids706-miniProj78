import argparse
import sqlite3
import time
import psutil
import resource


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

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS word_counts (
            filename TEXT PRIMARY KEY,
            word_count INTEGER
        )
    """
    )

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

    # Start tracking execution time and memory usage
    start_mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    start_time = time.time()

    # Count the words in the file
    word_count = count_words(args.filename)
    print(f"Word count: {word_count}")

    # Store the word count in the database
    store_word_count(args.filename, word_count, conn)

    # Measure CPU usage during this interval
    core_usage = psutil.cpu_percent(interval=1, percpu=True)
    num_cores = len(core_usage)
    total_usage = sum(core_usage)
    avg_cpu_usage = total_usage / num_cores

    # End tracking time and memory usage
    end_time = time.time()
    execution_time = end_time - start_time
    end_mem_usage = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    memory_used = (end_mem_usage - start_mem_usage) / 1024  # Convert to KB

    # Output the results
    print(f"Execution time: {execution_time:.6f} seconds")
    print(f"Average CPU core usage: {avg_cpu_usage:.2f}%")
    print(f"Memory used: {memory_used:.2f} KB")

    conn.close()


if __name__ == "__main__":
    main()
