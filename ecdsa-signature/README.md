# Asymmetric Cryptography & ECDSA Signatures

[Chinese Version / 中文文档](./README.zh.md)

A pure Python implementation of the Bitcoin Secp256k1 Elliptic Curve Digital Signature Algorithm (ECDSA).

Asymmetric cryptography forms the foundation of asset ownership in blockchain systems, ensuring that only the holder of a private key can authorize transactions, while any tampering or impersonation is instantly rejected by network nodes.

---

## Core Concepts & Math

### 1. Secp256k1 Elliptic Curve

Bitcoin uses the `secp256k1` elliptic curve equation:

$$y^2 \equiv x^3 + 7 \pmod p$$

Where $p = 2^{256} - 2^{32} - 977$.

- **Private Key**: A 256-bit random integer $d \in [1, N-1]$.
- **Public Key**: Derived via scalar multiplication $Q = d \times G$, where $G$ is the generator point. Due to Elliptic Curve Discrete Logarithm Problem (ECDLP), computing $d$ from $Q$ is computationally infeasible.
- **Address**: A short identifier derived by one-way hashing of the public key point.

### 2. ECDSA Sign & Verify Flow

- **Sign**:
  1. Computes hash $z = \text{SHA256}(m)$ of message $m$.
  2. Selects random nonce $k$, calculates curve point $R = k \times G = (x_1, y_1)$, setting $r = x_1 \pmod N$.
  3. Computes $s = k^{-1}(z + r \cdot d) \pmod N$.
  4. Outputs signature tuple $(r, s)$.

- **Verify**:
  1. Given public key $Q$, message $m$, and signature $(r, s)$.
  2. Computes $w = s^{-1} \pmod N$, $u_1 = z \cdot w \pmod N$, $u_2 = r \cdot w \pmod N$.
  3. Calculates curve point $P = u_1 \times G + u_2 \times Q$.
  4. Accepts if $x_P \equiv r \pmod N$.

---

## Directory Structure

```text
ecdsa-signature/
├── ecdsa_demo.py    # Secp256k1 & ECDSA pure Python source
├── README.md        # English documentation
└── README.zh.md     # Chinese documentation
```

---

## Quick Start

Run with standard Python 3:

```bash
cd ecdsa-signature
python3 ecdsa_demo.py
```

---

## Benchmark Execution Log

Execution output captured from `python3 ecdsa_demo.py`:

```text
==========================================
Bitcoin Secp256k1 ECDSA Signature Lab
==========================================

1. Generated Secp256k1 Keypair & Address:
   Private Key: 0xfd0eb86fb2c8f65b7e66e04cc7848e8e42ece9c03a6b3bacd5dc577727e73dc5
   Public Key X: 0x2bf8c5f83c5eefefbf202b09fd6a958938e68d3d40ba2ba9adaf2274d7a33e60
   Public Key Y: 0x08eaab7cc67f8cc59f510e59fffceed418a9d588a1507862dd85b5d30277ef92
   Derived Address: 63fbdf8f4cf34abf1b3f39df0e623ec39ffb4f67

2. Original Transaction Message:
   Message: 'Alice authorizes payment of 5 BTC to Bob'

3. Generated ECDSA Signature (r, s):
   r: 0x2156da9521b129133a86ba0f22a5ec6b5bc094d53729611b066ada559d88b9a4
   s: 0x33636e2482ba9f513547a21728cdb686a561ef8735f3deefa5ebae13371ac2b1

4. Signature Verification (Valid): True

5. Tamper Interception Test (Amount changed to 500 BTC): False

6. Impersonation Interception Test (Attacker using another key): False
==========================================
```

---

## Security Guarantees

1. **Unforgeability**: Computing $(r, s)$ without private key $d$ is as hard as brute-forcing 256-bit key space.
2. **Integrity**: Signature is tightly bound to message hash. Modifying message text invalidates verification (`False`).
3. **Non-repudiation**: Mathematical proof that transaction was authorized by private key owner.
