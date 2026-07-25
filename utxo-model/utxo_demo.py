import hashlib
from typing import List, Dict, Tuple

def hashlib_sha256(data: str) -> str:
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

class UTXO:
    def __init__(self, tx_id: str, output_index: int, amount: float, owner_address: str):
        self.tx_id = tx_id
        self.output_index = output_index
        self.amount = amount
        self.owner_address = owner_address

    def get_id(self) -> str:
        """获取该 UTXO 的唯一标识 (tx_id:output_index)"""
        return f"{self.tx_id}:{self.output_index}"

    def __repr__(self):
        return f"UTXO({self.get_id()} | 所有者: {self.owner_address} | 金额: {self.amount} BTC)"

class TransactionInput:
    def __init__(self, tx_id: str, output_index: int):
        self.tx_id = tx_id
        self.output_index = output_index

    def get_utxo_id(self) -> str:
        return f"{self.tx_id}:{self.output_index}"

class TransactionOutput:
    def __init__(self, amount: float, owner_address: str):
        self.amount = amount
        self.owner_address = owner_address

class Transaction:
    def __init__(self, inputs: List[TransactionInput], outputs: List[TransactionOutput], is_coinbase: bool = False):
        self.inputs = inputs
        self.outputs = outputs
        self.is_coinbase = is_coinbase
        self.tx_id = self.calculate_hash()

    def calculate_hash(self) -> str:
        content = ""
        for inp in self.inputs:
            content += inp.get_utxo_id()
        for outp in self.outputs:
            content += f"{outp.amount}:{outp.owner_address}"
        return hashlib_sha256(content)[:32]

class UTXOSet:
    def __init__(self):
        # 存储格式: utxo_id -> UTXO 对象
        self.utxos: Dict[str, UTXO] = {}

    def add_utxo(self, utxo: UTXO):
        self.utxos[utxo.get_id()] = utxo

    def get_balance(self, address: str) -> float:
        """计算指定地址的余额 (累加该地址持有的所有 UTXO)"""
        total = 0.0
        for utxo in self.utxos.values():
            if utxo.owner_address == address:
                total += utxo.amount
        return total

    def process_transaction(self, tx: Transaction) -> bool:
        """处理一笔交易：校验合法性，销毁旧 UTXO，产生新 UTXO"""
        if tx.is_coinbase:
            # 创世/挖矿奖励交易：无输入，直接产生输出
            for idx, outp in enumerate(tx.outputs):
                new_utxo = UTXO(tx.tx_id, idx, outp.amount, outp.owner_address)
                self.add_utxo(new_utxo)
            return True

        # 1. 双花校验与合法性校验：输入的 UTXO 是否存在于当前 UTXOSet 中
        input_sum = 0.0
        for inp in tx.inputs:
            utxo_id = inp.get_utxo_id()
            if utxo_id not in self.utxos:
                print(f"   [拒绝交易] 失败原因: 发现双花攻击或引用不存在的 UTXO ({utxo_id})！")
                return False
            input_sum += self.utxos[utxo_id].amount

        # 2. 资金守恒校验：Input 总额必须 >= Output 总额
        output_sum = sum(outp.amount for outp in tx.outputs)
        if input_sum < output_sum:
            print(f"   [拒绝交易] 失败原因: 输入余额不足！输入: {input_sum} BTC < 输出: {output_sum} BTC")
            return False

        # 3. 消费/销毁旧的 UTXO
        for inp in tx.inputs:
            utxo_id = inp.get_utxo_id()
            del self.utxos[utxo_id]

        # 4. 产生新的 UTXO 加入集合
        for idx, outp in enumerate(tx.outputs):
            new_utxo = UTXO(tx.tx_id, idx, outp.amount, outp.owner_address)
            self.add_utxo(new_utxo)

        miner_fee = input_sum - output_sum
        if miner_fee > 0:
            print(f"   [交易成功] 扣除矿工手续费: {miner_fee:.2f} BTC")
        return True

def print_utxo_pool(utxo_set: UTXOSet):
    print("\n当前全网有效 UTXO 账本集合:")
    if not utxo_set.utxos:
        print("  (当前没有未花费的 UTXO)")
    for utxo in utxo_set.utxos.values():
        print(f"  - {utxo}")

def main():
    print("==========================================")
    print("区块链 UTXO (未花费交易输出) 模型实验程序")
    print("==========================================")

    ledger = UTXOSet()

    # 1. 创世区块：通过 Coinbase 交易产生初始 50 BTC 奖励给 Alice
    print("\n1. 触发 Coinbase 创世交易 (系统奖励 50 BTC 给 Alice):")
    cb_out = TransactionOutput(amount=50.0, owner_address="Alice_Address")
    cb_tx = Transaction(inputs=[], outputs=[cb_out], is_coinbase=True)
    ledger.process_transaction(cb_tx)
    print_utxo_pool(ledger)
    print(f"  Alice 的余额: {ledger.get_balance('Alice_Address')} BTC")

    # 2. 交易一：Alice 发送 15 BTC 给 Bob，找零 34.5 BTC 给自己 (0.5 BTC 矿工费)
    print("\n2. 执行交易一 (Alice 支付 15 BTC 给 Bob，找零 34.5 BTC 给自己，0.5 BTC 矿工费):")
    alice_old_utxo_id = list(ledger.utxos.keys())[0] # 获取 Alice 的创世 UTXO
    tx1_in = TransactionInput(tx_id=cb_tx.tx_id, output_index=0)
    tx1_out1 = TransactionOutput(amount=15.0, owner_address="Bob_Address")
    tx1_out2 = TransactionOutput(amount=34.5, owner_address="Alice_Address") # 找零
    tx1 = Transaction(inputs=[tx1_in], outputs=[tx1_out1, tx1_out2])

    success1 = ledger.process_transaction(tx1)
    print(f"  交易执行结果: {success1}")
    print_utxo_pool(ledger)
    print(f"  Alice 当前余额: {ledger.get_balance('Alice_Address')} BTC")
    print(f"  Bob 当前余额:   {ledger.get_balance('Bob_Address')} BTC")

    # 3. 交易二：Bob 将刚拿到的 15 BTC 中的 10 BTC 支付给 Charlie (找零 5 BTC)
    print("\n3. 执行交易二 (Bob 支付 10 BTC 给 Charlie，找零 5 BTC 给自己):")
    # 找到 Bob 拥有的 UTXO
    bob_utxo_input = None
    for utxo in ledger.utxos.values():
        if utxo.owner_address == "Bob_Address":
            bob_utxo_input = TransactionInput(tx_id=utxo.tx_id, output_index=utxo.output_index)
            break

    tx2_out1 = TransactionOutput(amount=10.0, owner_address="Charlie_Address")
    tx2_out2 = TransactionOutput(amount=5.0, owner_address="Bob_Address")
    tx2 = Transaction(inputs=[bob_utxo_input], outputs=[tx2_out1, tx2_out2])

    success2 = ledger.process_transaction(tx2)
    print(f"  交易执行结果: {success2}")
    print_utxo_pool(ledger)
    print(f"  Alice 当前余额:   {ledger.get_balance('Alice_Address')} BTC")
    print(f"  Bob 当前余额:     {ledger.get_balance('Bob_Address')} BTC")
    print(f"  Charlie 当前余额: {ledger.get_balance('Charlie_Address')} BTC")

    # 4. 防双花攻击测试 (Double-Spend Detection):
    # 恶意攻击者尝试再次引用已经被销毁的创世 UTXO (Alice 创世 50 BTC) 发给 Eve
    print("\n4. 双花攻击拦截测试 (尝试再次使用已被销毁的 Alice 创世 50 BTC UTXO):")
    double_spend_in = TransactionInput(tx_id=cb_tx.tx_id, output_index=0) # 已被销毁
    double_spend_out = TransactionOutput(amount=50.0, owner_address="Eve_Address")
    fake_tx = Transaction(inputs=[double_spend_in], outputs=[double_spend_out])

    success_fake = ledger.process_transaction(fake_tx)
    print(f"  双花交易处理结果: {success_fake}")

    print("\n==========================================")
    print("实验完成：验证了 UTXO 销毁、找零生成与双花拦截流程！")
    print("==========================================")

if __name__ == "__main__":
    main()
