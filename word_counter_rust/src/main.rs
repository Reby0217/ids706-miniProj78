use rusqlite::{params, Connection, Result};  // Import the necessary modules from rusqlite
use sysinfo::{System, SystemExt, CpuExt, ProcessExt};  // Import ProcessExt for process memory tracking
use std::fs::File;
use std::io::{self, Read};
use std::time::Instant;
use std::thread::sleep;
use std::env; // For accessing command-line arguments

// Function to count words in a file
fn count_words(filename: &str) -> io::Result<usize> {
    let mut file = File::open(filename)?;
    let mut text = String::new();
    file.read_to_string(&mut text)?;
    Ok(text.split_whitespace().count())
}

// Function to store the word count in the SQLite database
fn store_word_count(filename: &str, word_count: usize, conn: &Connection) -> Result<()> {
    conn.execute(
        "CREATE TABLE IF NOT EXISTS word_counts (
            filename TEXT PRIMARY KEY,
            word_count INTEGER
        )",
        [],
    )?;

    conn.execute(
        "INSERT OR REPLACE INTO word_counts (filename, word_count) VALUES (?1, ?2)",
        params![filename, word_count],
    )?;
    Ok(())
}

fn main() -> Result<(), rusqlite::Error> {
    // Get command-line arguments
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: {} <filename>", args[0]);
        std::process::exit(1);
    }
    let filename = &args[1];

    // Start the system monitoring and time tracking
    let start_time = Instant::now();
    let mut sys = System::new_all();
    
    // Open SQLite connection
    let conn = Connection::open("word_counts.db")?;

    // Track the total CPU usage
    let mut total_usage = 0.0;

    // Word count operation
    let word_count = count_words(filename).unwrap();
    println!("Word count: {}", word_count);

    // Refresh system info before the operation to track memory usage
    sys.refresh_all();
    let process_memory_before = sys.processes().get(&sysinfo::get_current_pid().unwrap()).unwrap().memory();

    // Store word count in SQLite database
    store_word_count(filename, word_count, &conn)?;

    // Monitor CPU usage during operation
    sys.refresh_all();
    for cpu in sys.cpus() {
        total_usage += cpu.cpu_usage();
    }

    // Sleep for a bit to let the system gather CPU usage data
    sleep(System::MINIMUM_CPU_UPDATE_INTERVAL);
    
    // Get memory usage after storing the word count
    let process_memory_after = sys.processes().get(&sysinfo::get_current_pid().unwrap()).unwrap().memory();
    let memory_used_kb = process_memory_after - process_memory_before; // Memory in KB
    
    // Calculate execution time and final CPU usage
    let execution_time = start_time.elapsed();
    let avg_cpu_usage = total_usage / sys.cpus().len() as f32;

    // Output the results
    println!("Execution time: {}.{} seconds", execution_time.as_secs(), execution_time.subsec_millis());
    println!("Average CPU core usage: {:.2}%", avg_cpu_usage);
    println!("Memory used: {:.2} KB", memory_used_kb);

    Ok(())
}
