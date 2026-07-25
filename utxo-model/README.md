# UTXO (Unspent Transaction Output) Ledger Model

[Chinese Version / 中文文档](./README.zh.md)

A Python implementation of the Bitcoin UTXO (Unspent Transaction Output) ledger model.

Unlike traditional banking account systems with centralized balances, Bitcoin assets exist as discrete **UTXOs**. Every transaction destroys previous UTXOs (inputs) and mints new UTXOs (outputs).

---

## Core Concepts & Design

### 1. UTXO Model vs Account Balance Model

| Attribute | Account Balance Model (e.g. Ethereum) | UTXO Model (Bitcoin) |
| :--- | :--- | :--- |
| **Asset State** | Single balance number per account in global state tree | Collection of discrete unspent transaction outputs |
| **State Transition** | `Alice -= 10`, `Bob += 10` | Destroys Alice's old UTXO, mints Bob's new UTXO & Alice's change |
| **Parallelization** | Requires account locking to avoid race conditions | Lock-free parallel validation of independent UTXOs |
| **Privacy** | Global balance easily queryable | High privacy via dynamic single-use addresses |

### 2. Transaction Flow & Change Mechanism

1. **Coinbase Transaction**: Minting/mining rewards creating initial UTXOs without inputs.
2. **Inputs & Outputs**:
   - Inputs must fully reference and spend existing active UTXOs.
   - Outputs define recipient addresses and amounts.
3. **Change Generation**: Since UTXOs are spent atomically as a whole, change outputs return excess funds to the sender.
4. **Miner Fee**: $\text{Fee} = \sum \text{Inputs} - \sum \text{Outputs}$.

### 3. Double-Spending Attack Interception

Spent UTXOs are atomically deleted from the active `UTXOSet` database.

When an attacker attempts to double-spend a previously consumed UTXO, lookup against `UTXOSet` fails and the transaction is **immediately rejected (`False`)**.

---

## Directory Structure

```text
utxo-model/
├── utxo_demo.py     # Python source for UTXO ledger & transactions
├── README.md        # English documentation
└── README.zh.md     # Chinese documentation
```

---

## Quick Start

Run with standard Python 3:

```bash
cd utxo-model
python3 utxo_demo.py
```

---

## Benchmark Execution Log

Execution output captured from `python3 utxo_demo.py`:

```text
==========================================
Blockchain UTXO Ledger Model Lab
==========================================

1. Coinbase Transaction (50 BTC to Alice):

Current Active UTXOSet:
  - UTXO(98b5b6c6bdf1c4d0e352b2aa54c16987:0 | Owner: Alice_Address | Amount: 50.0 BTC)
  Alice Balance: 50.0 BTC

2. Transaction 1 (Alice sends 15 BTC to Bob, 34.5 BTC change, 0.5 BTC fee):
   [Success] Miner fee: 0.50 BTC
  Result: True

Current Active UTXOSet:
  - UTXO(ebae21a393ae1dad38b45e142adf8e4a:0 | Owner: Bob_Address | Amount: 15.0 BTC)
  - UTXO(ebae21a393ae1dad38b45e142adf8e4a:1 | Owner: Alice_Address | Amount: 34.5 BTC)
  Alice Balance: 34.5 BTC
  Bob Balance:   15.0 BTC

3. Transaction 2 (Bob sends 10 BTC to Charlie, 5 BTC change):
  Result: True

Current Active UTXOSet:
  - UTXO(ebae21a393ae1dad38b45e142adf8e4a:1 | Owner: Alice_Address | Amount: 34.5 BTC)
  - UTXO(411cfdb605fd99e48dd3406da867d3eb:0 | Owner: Charlie_Address | Amount: 10.0 BTC)
  - UTXO(411cfdb605fd99e48dd3406da867d3eb:1 | Owner: Bob_Address | Amount: 5.0 BTC)
  Alice Balance:   34.5 BTC
  Bob Balance:     5.0 BTC
  Charlie Balance: 10.0 BTC

4. Double-Spend Interception Test (Re-spending spent 50 BTC UTXO):
   [Rejected] Reason: Double-spend detected or referenced UTXO does not exist (98b5b6c6bdf1c4d0e352b2aa54c16987:0)!
  Double-Spend Result: False

==========================================
Lab Completed: Verified UTXO destruction, change generation & double-spend defense!
==========================================
```

---

## Conclusions

1. **No Account Balances**: Proves assets exist strictly as unspent transaction outputs.
2. **Atomic Destruction & Creation**: Transfers destroy inputs and mint new outputs.
3. **Double-Spend Protection**: Intercepted in $O(1)$ lookup time by checking `UTXOSet` set membership.
