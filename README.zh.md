# 区块链核心理论与底层算法实践 (Blockchain Theory & Practice)

本仓库包含区块链与比特币系统核心理论机制的完整代码实现与实验测试。通过 4 个独立的代码模块，从零剖析与验证区块链四大底层基石：共识算法、数据结构、密码学所有权与分布式账本模型。

---

## 5 大核心模块索引

| 模块名称 | 技术栈 | 解决的关键理论问题 | 源码及文档目录 |
| :--- | :--- | :--- | :--- |
| **1. PoW 哈希碰撞扫描器** | Rust (多线程 90% CPU) | 去中心化共识机制、出块难度控制与矿池分块计算 | [`hash/`](./hash/) |
| **2. 默克尔树 (Merkle Tree)** | Python | 交易数据高效汇总压缩与 SPV 轻节点 O(log N) 快速验证 | [`merkle-tree/`](./merkle-tree/) |
| **3. ECDSA 数字签名** | Python (Secp256k1) | 非对称加密与椭圆曲线数字签名，确立资产绝对所有权 | [`ecdsa-signature/`](./ecdsa-signature/) |
| **4. UTXO 账本模型** | Python | 离散交易输出流转、找零机制与防双花 (Double-Spend) 拦截 | [`utxo-model/`](./utxo-model/) |
| **5. PoS 权益证明与 Slashing** | Python | 质押加权抽签出块、权益共识演进与防双签惩罚机制 | [`pos-consensus/`](./pos-consensus/) |

---

## 目录结构地图

```text
blockchain-theory/
├── README.md               # 本仓库核心理论汇总说明文档
├── .gitignore              # 全局 Git 忽略规则配置
├── hash/                   # 模块 1: 基于 Rust 的高性能 PoW 哈希扫描器
│   ├── Cargo.toml
│   ├── run.sh              # 一键 Release 模式编译启动脚本
│   ├── results.csv         # 实测哈希碰撞导出数据
│   ├── README.md
│   └── src/main.rs
├── merkle-tree/            # 模块 2: 默克尔树与 SPV 验证
│   ├── merkle_tree.py
│   └── README.md
├── ecdsa-signature/        # 模块 3: Secp256k1 椭圆曲线数字签名
│   ├── ecdsa_demo.py
│   └── README.md
├── utxo-model/             # 模块 4: UTXO 账本与双花防护模型
│   ├── utxo_demo.py
│   └── README.md
└── pos-consensus/          # 模块 5: PoS 权益证明与 Slashing 机制
    ├── pos_demo.py
    └── README.md
```

---

## 模块运行指南

### 1. PoW 工作量证明模块 (Rust)

```bash
cd hash
./run.sh
```

### 2. 默克尔树 (Merkle Tree) 模块 (Python)

```bash
cd merkle-tree
python3 merkle_tree.py
```

### 3. ECDSA 椭圆曲线数字签名模块 (Python)

```bash
cd ecdsa-signature
python3 ecdsa_demo.py
```

### 4. UTXO 账本模型模块 (Python)

```bash
cd utxo-model
python3 utxo_demo.py
```

### 5. PoS 权益证明模块 (Python)

```bash
cd pos-consensus
python3 pos_demo.py
```
