import re


def parse_output(file_path):
    """
    Parses the output file and extracts word count, execution time, CPU usage, and memory used.
    """
    with open(file_path, "r") as f:
        content = f.read()

    word_count = int(re.search(r"Word count: (\d+)", content).group(1))
    execution_time = float(
        re.search(r"Execution time: ([\d\.]+) seconds", content).group(1)
    )
    avg_cpu_usage = float(
        re.search(r"Average CPU core usage: ([\d\.]+)%", content).group(1)
    )
    memory_used = float(re.search(r"Memory used: ([\d\.]+) KB", content).group(1))

    return {
        "word_count": word_count,
        "execution_time": execution_time,
        "avg_cpu_usage": avg_cpu_usage,
        "memory_used": memory_used,
    }


def calculate_ratio(python_val, rust_val):
    """
    Calculates the ratio between Python and Rust results.
    A ratio > 1 means Rust is higher; < 1 means Rust is lower.
    """
    if python_val == 0:
        return float("inf")  # If the Python value is 0, return an infinite ratio
    return rust_val / python_val


def generate_report(python_results, rust_results, report_file="performance_report.md"):
    """
    Generates a performance comparison report in markdown format, including
    ratio comparisons for execution time, CPU usage, and memory used.
    """
    execution_time_ratio = calculate_ratio(
        python_results["execution_time"], rust_results["execution_time"]
    )
    cpu_usage_ratio = calculate_ratio(
        python_results["avg_cpu_usage"], rust_results["avg_cpu_usage"]
    )
    memory_usage_ratio = calculate_ratio(
        python_results["memory_used"], rust_results["memory_used"]
    )

    with open(report_file, "w") as f:
        f.write("# Performance Comparison Report\n\n")

        f.write("## Word Count Results\n\n")
        f.write(f"- Python Word Count: {python_results['word_count']}\n")
        f.write(f"- Rust Word Count: {rust_results['word_count']}\n\n")

        f.write("## Execution Time Comparison\n\n")
        f.write(
            f"- Python Execution Time: {python_results['execution_time']} seconds\n"
        )
        f.write(f"- Rust Execution Time: {rust_results['execution_time']} seconds\n")
        
        if execution_time_ratio < 1:
            f.write(
                f"- **Execution Time**: Rust took {1 / execution_time_ratio:.2f} times less time than Python\n\n"
            )
        else:
            f.write(
                f"- **Execution Time**: Rust took {execution_time_ratio:.2f} times more time than Python\n\n"
            )

        f.write("## Average CPU Core Usage Comparison\n\n")
        f.write(f"- Python CPU Usage: {python_results['avg_cpu_usage']}%\n")
        f.write(f"- Rust CPU Usage: {rust_results['avg_cpu_usage']}%\n")
        
        if python_results['avg_cpu_usage'] == 0:
            f.write(f"- **CPU Usage**: Rust used negligible CPU compared to Python\n\n")
        elif cpu_usage_ratio < 1:
            f.write(
                f"- **CPU Usage**: Rust used {1 / cpu_usage_ratio:.2f} times less CPU than Python\n\n"
            )
        else:
            f.write(
                f"- **CPU Usage**: Rust used {cpu_usage_ratio:.2f} times more CPU than Python\n\n"
            )

        f.write("## Memory Usage Comparison\n\n")
        f.write(f"- Python Memory Used: {python_results['memory_used']} KB\n")
        f.write(f"- Rust Memory Used: {rust_results['memory_used']} KB\n")
        
        if python_results['memory_used'] == 0:
            f.write(f"- **Memory Usage**: Rust used significant memory compared to Python\n\n")
        elif memory_usage_ratio < 1:
            f.write(
                f"- **Memory Usage**: Rust used {1 / memory_usage_ratio:.2f} times less memory than Python\n\n"
            )
        else:
            f.write(
                f"- **Memory Usage**: Rust used {memory_usage_ratio:.2f} times more memory than Python\n\n"
            )

    print(f"Performance report generated: {report_file}")


def main():
    python_results = parse_output("python_results.txt")
    rust_results = parse_output("rust_results.txt")

    generate_report(python_results, rust_results)


if __name__ == "__main__":
    main()
