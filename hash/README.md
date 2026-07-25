# High-Performance Multi-Threaded SHA256 PoW Miner

[Chinese Version / 中文文档](./README.zh.md)

A high-performance Proof-of-Work (PoW) hash scanner implemented from scratch in **Rust**.

The program prepends a fixed prefix (default `"helloworld"`) and appends an incremental `salt` to compute SHA256 hashes, dynamically searching for hashes meeting specific leading zero targets to simulate core blockchain mining logic.

---

## Key Features

- **Zero GC Overhead**: Implemented in Rust with `--release` compiler optimization and native `sha2` cryptography primitives.
- **Dynamic 90% CPU Utilization**: Automatically detects total CPU logic cores and allocates 90% of available threads to maximize throughput.
- **Lock-Free Batching**: Worker threads use `AtomicU64` to claim salt ranges in batches, avoiding atomic lock contention.
- **Infinite Progress Target**:
  - Starts at leading zero target 1 and continuously advances to higher difficulties (1, 2, 3... N zeros).
  - Instantly logs and saves whenever historical leading zero records are broken.
  - Gracefully stops upon `Ctrl + C`.
- **Data Persistence & Immediate Flushing (`flush`)**:
  - Appends results into `results.csv` and retains history across runs.
  - Explicitly calls `.flush()` after every output to ensure real-time disk persistence.
- **Comprehensive Logging**: Generates `run.log` and `console.log` with real-time throughput metrics (H/s).

---

## Directory Structure

```text
hash/
├── Cargo.toml       # Project configuration (sha2, hex, chrono, ctrlc)
├── run.sh           # One-click Release build and execution script
├── README.md        # English documentation
├── README.zh.md     # Chinese documentation
├── results.csv      # Persistent benchmark output dataset
└── src/
    └── main.rs      # Core multi-threaded miner source code
```

---

## Quick Start

### Prerequisites

Ensure Rust and Cargo are installed:

```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

### Execution

Run via the built-in script:

```bash
cd hash
./run.sh
```

Or execute directly with Cargo:

```bash
cargo run --release
```

---

## Benchmark Case Study & Analysis (`results.csv`)

Captured output from a single continuous execution run:

| timestamp | target_zeros | salt | hash | elapsed_ms | hashes_tested |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `2026-07-24 20:45:24.742` | 1 | 28 | `09cb94ecf1ed...` | 0 | 28 |
| `2026-07-24 20:45:24.742` | 2 | 300145 | `005afd5d95f8...` | 0 | 145 |
| `2026-07-24 20:45:24.742` | 4 | 50437 | `000034b08352...` | 0 | 437 |
| `2026-07-24 20:45:24.746` | 5 | 106143 | `000001cca73c...` | 4 | 6143 |
| `2026-07-24 20:45:25.364` | 6 | 36737279 | `000000863236...` | 622 | 36787279 |
| `2026-07-24 20:45:35.662` | 7 | 651494081 | `00000005d0f8...` | 10920 | 651644081 |
| `2026-07-24 20:47:49.118` | 8 | 7374298388 | `000000008f46...` | 144376 | 7374048388 |

---

## Key Experimental Observations

Analysis of the `results.csv` benchmark data validates two fundamental PoW characteristics:

### 1. Exponential Difficulty Scaling & Search Space Growth

Each additional leading zero increases the target difficulty by a factor of 16 ($16^N$):
- **Leading Zeros 1 - 4**: Discovered within milliseconds (under tens of thousands of attempts).
- **Leading Zeros 6**: Salt expanded to 8 digits (`36737279`), taking 622 ms over 36 million hashes.
- **Leading Zeros 7**: Salt expanded to 9 digits (`651494081`), taking 10.9 seconds over 650 million hashes.
- **Leading Zeros 8**: Salt expanded to 10 digits (`7374298388`), taking **144 seconds (~2.4 minutes)** over **7.37 billion hashes**.

### 2. Difficulty Skip Phenomenon (e.g. Target Zero 3 Skipped)

Between lines 2 and 4 of the dataset:
- Right after target zero 2, the next logged result is **target zero 4** (`target_zeros = 4`), skipping zero 3 entirely.
- **Explanation**: A worker thread hit a lucky hash with 4 leading zeros (`000034b083...`) early in its assigned salt range (`salt = 50437`). Because 4 exceeded the current target 3, the system immediately logged this higher-difficulty hit and updated the global target to 5, bypassing the intermediate target 3.

---

## Mining Pool Theory Connection

The internal task distribution mechanism maps to distributed Bitcoin Mining Pools:

1. **Local Threads vs Pool Network**:
   - Main thread assigns salt ranges to 90% CPU worker threads, mirroring how a Mining Pool server delegates nonce ranges to thousands of mining rigs.
2. **Difficulty Targets**:
   - Demonstrates how exponential hash difficulty regulates global block time.
3. **Shares Mechanism**:
   - Illustrates how lower-difficulty intermediate hits (Shares) allow pools to measure miner hash contributions and distribute rewards fairly.
