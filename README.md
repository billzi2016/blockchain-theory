# Blockchain Theory & Practice (Core Algorithms & Consensus)

[Chinese Version / 中文文档](./README.zh.md)

This repository contains a clean, from-scratch implementation of core blockchain algorithms and consensus theory. Through 5 distinct modules written in Rust and Python, it dissects and verifies the fundamental pillars of blockchain technology: consensus, cryptographic ownership, data structures, and state management.

---

## 5 Core Modules Index

| Module Name | Tech Stack | Core Theory & Problems Solved | Source & Docs |
| :--- | :--- | :--- | :--- |
| **1. PoW Hash Miner** | Rust (Multi-threaded 90% CPU) | Decentralized consensus, difficulty adjustment, and pool task batching | [`hash/`](./hash/) |
| **2. Merkle Tree** | Python | Binary hash tree, data compression, and SPV light client $O(\log N)$ verification | [`merkle-tree/`](./merkle-tree/) |
| **3. ECDSA Signatures** | Python (Secp256k1) | Asymmetric cryptography, public key derivation, and transaction ownership authorization | [`ecdsa-signature/`](./ecdsa-signature/) |
| **4. UTXO Ledger Model** | Python | Unspent transaction output model, change generation, and Double-Spend prevention | [`utxo-model/`](./utxo-model/) |
| **5. PoS Consensus & Slashing** | Python | Weighted proposer selection, staking rewards, and Slashing penalty for double-signing | [`pos-consensus/`](./pos-consensus/) |

---

## Directory Map

```text
blockchain-theory/
├── README.md               # Main English documentation
├── README.zh.md            # Main Chinese documentation
├── .gitignore              # Global Git ignore rules
├── hash/                   # Module 1: High-performance Rust PoW miner
│   ├── Cargo.toml
│   ├── run.sh              # Release mode build & run script
│   ├── results.csv         # Benchmark output dataset
│   ├── README.md           # Module English docs
│   ├── README.zh.md        # Module Chinese docs
│   └── src/main.rs
├── merkle-tree/            # Module 2: Merkle Tree & SPV Proofs
│   ├── merkle_tree.py
│   ├── README.md
│   └── README.zh.md
├── ecdsa-signature/        # Module 3: Secp256k1 ECDSA Digital Signatures
│   ├── ecdsa_demo.py
│   ├── README.md
│   └── README.zh.md
├── utxo-model/             # Module 4: UTXO Ledger & Double-Spend Defense
│   ├── utxo_demo.py
│   ├── README.md
│   └── README.zh.md
└── pos-consensus/          # Module 5: PoS Consensus & Slashing Mechanism
    ├── pos_demo.py
    ├── README.md
    └── README.zh.md
```

---

## Quick Start Guide

### 1. PoW Consensus Module (Rust)

```bash
cd hash
./run.sh
```

### 2. Merkle Tree & SPV Module (Python)

```bash
cd merkle-tree
python3 merkle_tree.py
```

### 3. ECDSA Digital Signature Module (Python)

```bash
cd ecdsa-signature
python3 ecdsa_demo.py
```

### 4. UTXO Ledger Model Module (Python)

```bash
cd utxo-model
python3 utxo_demo.py
```

### 5. PoS Consensus & Slashing Module (Python)

```bash
cd pos-consensus
python3 pos_demo.py
```
