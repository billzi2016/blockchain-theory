# Proof of Stake (PoS) Consensus & Slashing Lab

[Chinese Version / 中文文档](./README.zh.md)

A Python implementation of Proof of Stake (PoS) consensus algorithm and Slashing penalty mechanism.

PoS is widely adopted by modern blockchains (e.g. Ethereum 2.0, Cardano, Solana), replacing energy-intensive PoW hash calculations with economic staking.

---

## Core Concepts & Design

### 1. PoW vs PoS Comparison

| Attribute | PoW (Proof of Work) | PoS (Proof of Stake) |
| :--- | :--- | :--- |
| **Block Right Factor** | Physical CPU/GPU/ASIC hash speed | Amount of tokens staked in validator pool |
| **Resource Consumption** | Very High (Electricity & Hardware) | Very Low (Standard network communication) |
| **Proposer Selection** | Fastest node to find leading zero hash | Weighted random draw based on stake ratio |
| **Security Mechanism** | 51% Physical Hashrate Attack Cost | 51% Economic Acquisition Cost & Slashing |

### 2. Nothing at Stake Problem

In naive PoS algorithms, signing blocks on multiple fork branches costs zero physical energy. Because validators can vote on all branches without penalty, they are incentivized to support all forks, preventing network consensus.

### 3. Slashing Penalty Solution

To eliminate Nothing at Stake risk, modern PoS networks introduce **Slashing**:
- **Double Signing Detection**: If a validator signs two conflicting blocks at the same block height;
- **Stake Forfeiture**: Cryptographic proof triggers automatic **confiscation of part or all of their staked tokens**;
- **Eviction**: Sets validator status to `Slashed` and permanently ejects them from the active validator pool.

---

## Directory Structure

```text
pos-consensus/
├── pos_demo.py      # Python source for PoS staking & Slashing
├── README.md        # English documentation
└── README.zh.md     # Chinese documentation
```

---

## Quick Start

Run with standard Python 3:

```bash
cd pos-consensus
python3 pos_demo.py
```

---

## Benchmark Execution Log

Execution output captured from `python3 pos_demo.py`:

```text
==========================================
Blockchain PoS & Slashing Lab
==========================================

1. Validators Staking Phase:
   Initial Active Pool Stake: 1000.0 Tokens
   Initial Weights:
     - Alice: 500.0 Tokens (50.0%)
     - Bob: 300.0 Tokens (30.0%)
     - Charlie: 200.0 Tokens (20.0%)

2. Running 1000 Rounds of PoS Selection:

   Results after 1000 rounds:
     - Validator: Alice    | Stake: 1450.0 Tokens | Blocks:  475 | Rewards:  950.0 | Status: Active
       Actual Block Ratio: 47.50% (Expected: ~48.3%)
     - Validator: Bob      | Stake:  906.0 Tokens | Blocks:  303 | Rewards:  606.0 | Status: Active
       Actual Block Ratio: 30.30% (Expected: ~30.2%)
     - Validator: Charlie  | Stake:  644.0 Tokens | Blocks:  222 | Rewards:  444.0 | Status: Active
       Actual Block Ratio: 22.20% (Expected: ~21.5%)

3. Security Attack Test (Charlie attempts Double-Signing on forks):

   [SECURITY ALERT - SLASHING TRIGGERED] Validator 'Charlie' severe violation!
   Reason: Malicious double-signing on conflicting fork chains at same height
   Action: Forfeited 644.0 staked tokens and permanently evicted from validator pool!

4. Validator Status After Slashing:
   - Validator: Alice    | Stake: 1450.0 Tokens | Blocks:  475 | Rewards:  950.0 | Status: Active
   - Validator: Bob      | Stake:  906.0 Tokens | Blocks:  303 | Rewards:  606.0 | Status: Active
   - Validator: Charlie  | Stake:    0.0 Tokens | Blocks:  222 | Rewards:  444.0 | Status: Slashed

5. Running 100 Rounds After Eviction:

   Final Validator Settlement:
   - Validator: Alice    | Stake: 1584.0 Tokens | Blocks:  542 | Rewards: 1084.0 | Status: Active
   - Validator: Bob      | Stake:  972.0 Tokens | Blocks:  336 | Rewards:  672.0 | Status: Active
   - Validator: Charlie  | Stake:    0.0 Tokens | Blocks:  222 | Rewards:  444.0 | Status: Slashed

==========================================
Lab Completed: Verified PoS weighted proposer selection & Slashing defense!
==========================================
```

---

## Conclusions

1. **Statistical Alignment**: 1000-round simulation confirms block proposal frequencies closely match initial stake ratios (Alice ~50%, Bob ~30%, Charlie ~20%).
2. **Economic Defense**: Confiscating Charlie's 644.0 tokens and evicting his node ensures attack costs far exceed potential gains.
