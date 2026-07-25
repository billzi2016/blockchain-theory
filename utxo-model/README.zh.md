# UTXO (未花费交易输出) 账本模型区块链实验

基于 Python 实现的比特币 UTXO (Unspent Transaction Output) 账本模型实验程序。

在比特币网络中，并没有传统银行或账户系统中记录的“余额数字”，所有的资产都以 **UTXO (未花费交易输出)** 的形式离散存在。每一笔交易都是对旧 UTXO 的销毁，并同时熔炼产生新的 UTXO。

---

## 核心原理与设计机制

### 1. UTXO 模型 vs 传统账户余额模型

| 维度 | 传统账户余额模型 (Account-based) | UTXO 模型 (Bitcoin) |
| :--- | :--- | :--- |
| **资产记录形态** | 全局状态树中记录单个账户的总金额 | 分散存在的一张张“未花费的钱票/硬币” |
| **交易处理方式** | `Alice -= 10`, `Bob += 10` | 销毁 Alice 旧的 UTXO，产生 Bob 的新 UTXO 和 Alice 的找零 UTXO |
| **并行验证能力** | 需对账号加锁，防死锁导致并发瓶颈 | 各 UTXO 独立存在，支持无锁极致并行校验 |
| **隐私保护能力** | 单一账户余额完全暴露 | 地址可随时动态更换，天然具备更高隐蔽性 |

### 2. 交易流转与找零机制

1. **Coinbase 交易**：矿工通过打包区块获得系统创世/出块奖励，无输入，直接产生最初的 UTXO。
2. **交易输入 (Inputs) 与输出 (Outputs)**：
   - 交易输入必须完全引用并一次性消费**已存在且未被使用的旧 UTXO**。
   - 交易输出指定新的接收者地址与金额。
3. **找零 (Change)**：由于 UTXO 必须作为一个整体被一次性消费，若转账金额小于该 UTXO 额度，必须创建一个指向转出者自己的找零输出。
4. **矿工费 (Miner Fee)**：$\text{Fee} = \sum \text{Inputs} - \sum \text{Outputs}$。

### 3. 双花攻击 (Double-Spending Attack) 拦截

在 UTXO 集合中，已被消费过的 UTXO 会在原子更新中被从 `UTXOSet` 数据库中彻底物理删除。

当恶意攻击者尝试重复使用同一个已消费的 UTXO 发起二次支付时，节点查询 `UTXOSet` 会发现该标识不存在，交易会被**瞬时强行拒绝并拦截 (`False`)**。

---

## 项目文件结构

```text
utxo-model/
├── utxo_demo.py     # UTXO 账本集合与交易流转纯 Python 源码
└── README.md        # 实验说明文档
```

---

## 快速开始

环境需求为标准 Python 3：

```bash
cd utxo-model
python3 utxo_demo.py
```

---

## 真实运行结果展示

实测运行 `python3 utxo_demo.py` 捕获的完整输出如下：

```text
==========================================
区块链 UTXO (未花费交易输出) 模型实验程序
==========================================

1. 触发 Coinbase 创世交易 (系统奖励 50 BTC 给 Alice):

当前全网有效 UTXO 账本集合:
  - UTXO(98b5b6c6bdf1c4d0e352b2aa54c16987:0 | 所有者: Alice_Address | 金额: 50.0 BTC)
  Alice 的余额: 50.0 BTC

2. 执行交易一 (Alice 支付 15 BTC 给 Bob，找零 34.5 BTC 给自己，0.5 BTC 矿工费):
   [交易成功] 扣除矿工手续费: 0.50 BTC
  交易执行结果: True

当前全网有效 UTXO 账本集合:
  - UTXO(ebae21a393ae1dad38b45e142adf8e4a:0 | 所有者: Bob_Address | 金额: 15.0 BTC)
  - UTXO(ebae21a393ae1dad38b45e142adf8e4a:1 | 所有者: Alice_Address | 金额: 34.5 BTC)
  Alice 当前余额: 34.5 BTC
  Bob 当前余额:   15.0 BTC

3. 执行交易二 (Bob 支付 10 BTC 给 Charlie，找零 5 BTC 给自己):
  交易执行结果: True

当前全网有效 UTXO 账本集合:
  - UTXO(ebae21a393ae1dad38b45e142adf8e4a:1 | 所有者: Alice_Address | 金额: 34.5 BTC)
  - UTXO(411cfdb605fd99e48dd3406da867d3eb:0 | 所有者: Charlie_Address | 金额: 10.0 BTC)
  - UTXO(411cfdb605fd99e48dd3406da867d3eb:1 | 所有者: Bob_Address | 金额: 5.0 BTC)
  Alice 当前余额:   34.5 BTC
  Bob 当前余额:     5.0 BTC
  Charlie 当前余额: 10.0 BTC

4. 双花攻击拦截测试 (尝试再次使用已被销毁的 Alice 创世 50 BTC UTXO):
   [拒绝交易] 失败原因: 发现双花攻击或引用不存在的 UTXO (98b5b6c6bdf1c4d0e352b2aa54c16987:0)！
  双花交易处理结果: False

==========================================
实验完成：验证了 UTXO 销毁、找零生成与双花拦截流程！
==========================================
```

---

## 结论

实验完整演示了比特币底层核心资产流转方式：
1. 没有余额状态，只有未消费输出列表。
2. 转账即旧 UTXO 销毁与新 UTXO 诞生。
3. 双花攻击被节点基于 UTXO 集合唯一性秒级识别与拒绝。
