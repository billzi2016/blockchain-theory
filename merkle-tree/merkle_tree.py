import hashlib
from typing import List, Tuple, Optional

def hashlib_sha256(data: str) -> str:
    """计算字符串的 SHA256 哈希值 (十六进制)"""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

class MerkleTree:
    def __init__(self, transactions: List[str]):
        self.transactions = transactions
        self.leaves = [hashlib_sha256(tx) for tx in transactions]
        self.layers: List[List[str]] = [self.leaves]
        self.build_tree()

    def build_tree(self):
        """逐层向上构建 Merkle Tree"""
        current_layer = self.leaves
        while len(current_layer) > 1:
            next_layer = []
            # 如果节点数为奇数，复制最后一个节点凑成偶数
            if len(current_layer) % 2 != 0:
                current_layer.append(current_layer[-1])

            for i in range(0, len(current_layer), 2):
                combined = current_layer[i] + current_layer[i + 1]
                parent_hash = hashlib_sha256(combined)
                next_layer.append(parent_hash)
            
            self.layers.append(next_layer)
            current_layer = next_layer

    def get_root(self) -> str:
        """获取 Merkle Root"""
        return self.layers[-1][0] if self.layers else ""

    def get_proof(self, tx_index: int) -> List[Tuple[str, str]]:
        """
        生成指定交易的 Merkle Proof (路径证明)
        返回包含 (sibling_hash, direction) 的列表，direction 为 'left' 或 'right'
        """
        if tx_index < 0 or tx_index >= len(self.transactions):
            raise ValueError("交易索引超出范围")

        proof = []
        idx = tx_index

        for layer in self.layers[:-1]:
            # 如果当前层节点数为奇数，且 idx 是最后一个元素，复制它
            layer_copy = list(layer)
            if len(layer_copy) % 2 != 0:
                layer_copy.append(layer_copy[-1])

            if idx % 2 == 0:
                sibling_idx = idx + 1
                direction = 'right'
            else:
                sibling_idx = idx - 1
                direction = 'left'

            proof.append((layer_copy[sibling_idx], direction))
            idx //= 2

        return proof

def verify_proof(tx_data: str, proof: List[Tuple[str, str]], root: str) -> bool:
    """验证交易和 Merkle Proof 是否匹配根节点 Root"""
    current_hash = hashlib_sha256(tx_data)

    for sibling_hash, direction in proof:
        if direction == 'right':
            combined = current_hash + sibling_hash
        else:
            combined = sibling_hash + current_hash
        current_hash = hashlib_sha256(combined)

    return current_hash == root


def main():
    print("==========================================")
    print("区块链 Merkle Tree (默克尔树) 实验程序")
    print("==========================================")

    # 准备一组模拟区块交易
    transactions = ["tx1: Alice -> Bob (10 BTC)",
                    "tx2: Bob -> Charlie (5 BTC)",
                    "tx3: Charlie -> David (2 BTC)",
                    "tx4: David -> Eve (1 BTC)",
                    "tx5: Eve -> Frank (0.5 BTC)"]

    print(f"\n1. 区块中原始交易列表 (共 {len(transactions)} 笔):")
    for i, tx in enumerate(transactions):
        print(f"  [{i}] {tx}")

    # 构建 Merkle Tree
    tree = MerkleTree(transactions)

    print("\n2. Merkle Tree 结构构建层级:")
    for layer_idx, layer in enumerate(tree.layers):
        print(f"  层级 {layer_idx} (节点数: {len(layer)}):")
        for node_idx, node_hash in enumerate(layer):
            print(f"    - 节点 [{node_idx}]: {node_hash}")

    merkle_root = tree.get_root()
    print(f"\n3. 计算得到的 Merkle Root (默克尔根):")
    print(f"   Root: {merkle_root}")

    # 4. 生成与验证针对 tx3 的 Merkle Proof
    target_idx = 2
    target_tx = transactions[target_idx]
    proof = tree.get_proof(target_idx)

    print(f"\n4. 为交易 [{target_idx}] '{target_tx}' 生成的 Merkle Proof 路径:")
    for step_idx, (sibling_hash, direction) in enumerate(proof):
        print(f"   步骤 {step_idx + 1}: 兄弟节点哈希 ({direction}) -> {sibling_hash}")

    # 进行合法验证
    is_valid = verify_proof(target_tx, proof, merkle_root)
    print(f"\n5. 验证交易真实性结果 (合法交易): {is_valid}")

    # 6. 防篡改测试：修改交易数据再验证
    fake_tx = "tx3: Charlie -> David (200 BTC)"
    is_tampered_valid = verify_proof(fake_tx, proof, merkle_root)
    print(f"\n6. 验证防篡改拦截结果 (被篡改的交易): {is_tampered_valid}")
    print("==========================================")

if __name__ == "__main__":
    main()
