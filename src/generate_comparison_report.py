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
        
        if execution_time_ratio == float("inf"):
            f.write(
                f"- **Execution Time**: Rust execution time was significantly higher than Python\n\n"
            )
        elif execution_time_ratio < 1:
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
            f.write(f"- **CPU Usage**: Python reported negligible CPU usage\n\n")
        elif cpu_usage_ratio == float("inf"):
            f.write(f"- **CPU Usage**: Rust used significantly more CPU than Python\n\n")
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
            f.write(f"- **Memory Usage**: Python reported negligible memory usage\n\n")
        elif memory_usage_ratio == float("inf"):
            f.write(f"- **Memory Usage**: Rust used significantly more memory than Python\n\n")
        elif memory_usage_ratio < 1:
            f.write(
                f"- **Memory Usage**: Rust used {1 / memory_usage_ratio:.2f} times less memory than Python\n\n"
            )
        else:
            f.write(
                f"- **Memory Usage**: Rust used {memory_usage_ratio:.2f} times more memory than Python\n\n"
            )

    print(f"Performance report generated: {report_file}")
