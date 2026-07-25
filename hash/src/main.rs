use chrono::Local;
use sha2::{Digest, Sha256};
use std::fs::{OpenOptions, File};
use std::io::Write;
use std::sync::atomic::{AtomicBool, AtomicU64, AtomicUsize, Ordering};
use std::sync::{Arc, Mutex};
use std::thread;
use std::time::Instant;

const PREFIX: &str = "helloworld";
const BATCH_SIZE: u64 = 50_000;

struct LogWriter {
    csv_file: File,
    log_file: File,
}

impl LogWriter {
    fn new() -> Self {
        let mut csv_file = OpenOptions::new()
            .create(true)
            .append(true)
            .open("results.csv")
            .unwrap();

        // 仅当文件为空时写入 CSV 表头，保留已有历史数据
        if csv_file.metadata().map(|m| m.len() == 0).unwrap_or(false) {
            writeln!(
                csv_file,
                "timestamp,target_zeros,salt,hash,elapsed_ms,hashes_tested"
            )
            .unwrap();
            csv_file.flush().unwrap();
        }

        let log_file = OpenOptions::new()
            .create(true)
            .append(true)
            .open("run.log")
            .unwrap();

        LogWriter { csv_file, log_file }
    }

    fn log_result(&mut self, zeros: usize, salt: u64, hash_str: &str, elapsed_ms: u128, total_hashes: u64) {
        let time_str = Local::now().format("%Y-%m-%d %H:%M:%S.%3f").to_string();
        let log_line = format!(
            "[{}] [成功] 目标前导零: {} | Salt: {} | Hash: {} | 耗时: {} ms | 总测试 Hash 数: {}",
            time_str, zeros, salt, hash_str, elapsed_ms, total_hashes
        );

        println!("{}", log_line);

        // 写入 run.log
        writeln!(self.log_file, "{}", log_line).ok();
        self.log_file.flush().ok();

        // 写入 results.csv
        writeln!(
            self.csv_file,
            "{},{},{},{},{},{}",
            time_str, zeros, salt, hash_str, elapsed_ms, total_hashes
        )
        .ok();
        self.csv_file.flush().ok();
    }

    fn log_info(&mut self, message: &str) {
        let time_str = Local::now().format("%Y-%m-%d %H:%M:%S").to_string();
        let log_line = format!("[{}] [INFO] {}", time_str, message);
        println!("{}", log_line);
        writeln!(self.log_file, "{}", log_line).ok();
        self.log_file.flush().ok();
    }
}

fn count_leading_zeros_hex(hash: &[u8]) -> usize {
    let mut zeros = 0;
    for &byte in hash {
        let high = byte >> 4;
        let low = byte & 0x0F;
        if high == 0 {
            zeros += 1;
            if low == 0 {
                zeros += 1;
            } else {
                break;
            }
        } else {
            break;
        }
    }
    zeros
}

fn main() {
    let running = Arc::new(AtomicBool::new(true));
    let r = running.clone();

    ctrlc::set_handler(move || {
        println!("\n[!] 收到 Ctrl+C 终止信号，正在保存数据并优雅退出...");
        r.store(false, Ordering::SeqCst);
    })
    .expect("设置 Ctrl+C 监听失败");

    // 计算 CPU 线程数（使用 90% 线程）
    let total_threads = thread::available_parallelism()
        .map(|n| n.get())
        .unwrap_or(4);
    let worker_threads = ((total_threads as f64 * 0.9).round() as usize).max(1);

    let writer = Arc::new(Mutex::new(LogWriter::new()));

    {
        let mut w = writer.lock().unwrap();
        w.log_info("==========================================");
        w.log_info(&format!(
            "启动 PoW Hash 扫描程序 (前缀: '{}')",
            PREFIX
        ));
        w.log_info(&format!(
            "检测到系统逻辑核心数: {}，启用 90% 线程数: {}",
            total_threads, worker_threads
        ));
        w.log_info("按 Ctrl+C 可随时停止程序运行。结果将实时保存至 results.csv 与 run.log");
        w.log_info("==========================================");
    }

    let global_salt = Arc::new(AtomicU64::new(0));
    let target_zeros = Arc::new(AtomicUsize::new(1));
    let total_hashes_counter = Arc::new(AtomicU64::new(0));
    let start_time = Instant::now();

    let mut handles = Vec::new();

    for _thread_id in 0..worker_threads {
        let running_flag = running.clone();
        let global_salt_counter = global_salt.clone();
        let target_zeros_counter = target_zeros.clone();
        let total_hashes_counter = total_hashes_counter.clone();
        let writer_clone = writer.clone();

        let handle = thread::spawn(move || {
            let mut hasher_base = Sha256::new();
            hasher_base.update(PREFIX.as_bytes());

            while running_flag.load(Ordering::Relaxed) {
                let start_salt = global_salt_counter.fetch_add(BATCH_SIZE, Ordering::Relaxed);
                let end_salt = start_salt + BATCH_SIZE;

                for salt in start_salt..end_salt {
                    if !running_flag.load(Ordering::Relaxed) {
                        break;
                    }

                    // 快速拼接 salt 数字转 string 后的 hash
                    let mut hasher = hasher_base.clone();
                    hasher.update(salt.to_string().as_bytes());
                    let result = hasher.finalize();

                    let current_zeros = count_leading_zeros_hex(&result);
                    let required_zeros = target_zeros_counter.load(Ordering::Relaxed);

                    if current_zeros >= required_zeros {
                        // 发现符合当前目标或者更高难度的 hash
                        let mut w = writer_clone.lock().unwrap();
                        let newest_required = target_zeros_counter.load(Ordering::Relaxed);
                        if current_zeros >= newest_required {
                            let hash_hex = hex::encode(result);
                            let elapsed_ms = start_time.elapsed().as_millis();
                            let total_h = total_hashes_counter.load(Ordering::Relaxed) + (salt - start_salt);

                            w.log_result(current_zeros, salt, &hash_hex, elapsed_ms, total_h);

                            // 提升下一个目标难度
                            target_zeros_counter.store(current_zeros + 1, Ordering::Relaxed);
                        }
                    }
                }

                total_hashes_counter.fetch_add(BATCH_SIZE, Ordering::Relaxed);
            }
        });

        handles.push(handle);
    }

    // 主线程等待所有 worker 线程退出
    for handle in handles {
        handle.join().ok();
    }

    let elapsed = start_time.elapsed();
    let total_hashes = total_hashes_counter.load(Ordering::Relaxed);
    let hash_rate = if elapsed.as_secs_f64() > 0.0 {
        total_hashes as f64 / elapsed.as_secs_f64()
    } else {
        0.0
    };

    let mut w = writer.lock().unwrap();
    w.log_info("==========================================");
    w.log_info(&format!(
        "程序停止。总运行时间: {:.2?} | 总哈希计算数: {} | 平均算力: {:.2} H/s",
        elapsed, total_hashes, hash_rate
    ));
    w.log_info("所有结果与日志已保存完成。");
    w.log_info("==========================================");
}
