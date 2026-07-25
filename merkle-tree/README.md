# Merkle Tree & SPV Verification Blockchain Lab

[Chinese Version / 中文文档](./README.zh.md)

A Python implementation of Merkle Tree construction and Simple Payment Verification (SPV) Merkle Proof validation.

The Merkle Tree is a foundational data structure in blockchains (e.g. Bitcoin, Ethereum), providing efficient, tamper-proof aggregation and validation of transaction datasets.

---

## Core Concepts & Mechanisms

### 1. Merkle Tree Construction

1. **Leaf Hash Computation**: Each transaction in a block is hashed via SHA256 to form leaf nodes.
2. **Pairwise Hashing Upwards**:
   - Adjacent node hashes are concatenated and hashed (`Hash(Node_A + Node_B)`) to compute parent nodes.
   - If an odd number of nodes exists at any level, the last node is duplicated to complete the pair.
3. **Merkle Root Generation**: The process repeats until a single root hash (Merkle Root) is generated and stored in the Block Header.

### 2. Merkle Proof & SPV Validation

Light clients (SPV nodes) do not download full blockchain transactions; they only store 80-byte Block Headers with Merkle Roots.

To verify whether a transaction exists in a block:
- Full nodes supply the transaction's **Merkle Proof (Audit Path)**.
- Light clients compute hashes upwards using the transaction data and sibling hashes in the proof.
- If the final computed hash matches the Merkle Root in the Block Header, the transaction is verified as valid and untampered.
- Time and space complexity: **O(log N)**.

---

## Directory Structure

```text
merkle-tree/
├── merkle_tree.py   # Python source for Merkle Tree & SPV validation
├── README.md        # English documentation
└── README.zh.md     # Chinese documentation
```

---

## Quick Start

Run with standard Python 3 (zero external dependencies):

```bash
cd merkle-tree
python3 merkle_tree.py
```

---

## Benchmark Execution Log

Execution output captured from `python3 merkle_tree.py`:

```text
==========================================
Blockchain Merkle Tree Lab
==========================================

1. Block Transactions (5 txs):
  [0] tx1: Alice -> Bob (10 BTC)
  [1] tx2: Bob -> Charlie (5 BTC)
  [2] tx3: Charlie -> David (2 BTC)
  [3] tx4: David -> Eve (1 BTC)
  [4] tx5: Eve -> Frank (0.5 BTC)

2. Merkle Tree Structure:
  Layer 0 (Nodes: 6):
    - Node [0]: 2e95c04c82daa6f5255c20a822f70d5cfe3333e0d0a28202116ef38ce8946b54
    - Node [1]: 36590d9231d02ba1964fc65a65a9cfe56ac6b613028ed554e9e3fcc418bf0f37
    - Node [2]: 61acc8426ba9360ced0005b80e86db74d1ee82121761d7a855408c2031b5df30
    - Node [3]: 0bb7e8c826444fb6f08d956e3a2586bbb49b19a9bc4091900c4ba12e586bea0d
    - Node [4]: f5146327303ceba5fe9dfbf447bfc26b87416e165ba46b495cdbe3ea29a4c2f4
    - Node [5]: f5146327303ceba5fe9dfbf447bfc26b87416e165ba46b495cdbe3ea29a4c2f4
  Layer 1 (Nodes: 4):
    - Node [0]: 5bed1af37f39a63410825e4594016dbd232418b168228ce7a76eb965bb52122b
    - Node [1]: cc64fdb7b710890b84cc8792a1fee32bb1cd56bc8407be9e44992fb0d30809a6
    - Node [2]: 3c564b8466ec7433aef7e4ee40bbb5f96f0796ad47f7e769319c4f4fd8a10f69
    - Node [3]: 3c564b8466ec7433aef7e4ee40bbb5f96f0796ad47f7e769319c4f4fd8a10f69
  Layer 2 (Nodes: 2):
    - Node [0]: 53ad0400b5ccb44e4c1a8d3d2292f60d6afc5572813841f0811c40d5109e4bd9
    - Node [1]: 6b22b774ae7c2b41c33611d5838ae462b84796dd35eda1b9382441da395334c5
  Layer 3 (Nodes: 1):
    - Node [0]: d554c26564cf1c5cf214804418d8479a82ec103b90d28996d7e41f4e3e72e363

3. Merkle Root:
   Root: d554c26564cf1c5cf214804418d8479a82ec103b90d28996d7e41f4e3e72e363

4. Merkle Proof Path for [2] 'tx3: Charlie -> David (2 BTC)':
   Step 1: Sibling (right) -> 0bb7e8c826444fb6f08d956e3a2586bbb49b19a9bc4091900c4ba12e586bea0d
   Step 2: Sibling (left)  -> 5bed1af37f39a63410825e4594016dbd232418b168228ce7a76eb965bb52122b
   Step 3: Sibling (right) -> 6b22b774ae7c2b41c33611d5838ae462b84796dd35eda1b9382441da395334c5

5. Transaction Verification (Valid tx): True

6. Tamper Defense Test (Modified tx): False
==========================================
```

---

## Conclusions

1. **Odd Duplication**: Demonstrates how 5 transactions (odd) duplicate node 4 (`tx5`) into node 5 to preserve binary tree invariants.
2. **Efficient Verification**: Validates `tx3` with just 3 sibling hashes without downloading full transaction history.
3. **Tamper Resistance**: Modifying transfer amount from 2 BTC to 200 BTC alters hash propagation, resulting in verification failure (`False`).
