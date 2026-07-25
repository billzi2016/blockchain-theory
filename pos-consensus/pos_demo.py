import random
from typing import List, Dict, Optional

class Validator:
    def __init__(self, name: str, stake: float):
        self.name = name
        self.stake = stake
        self.blocks_produced = 0
        self.rewards = 0.0
        self.is_slashed = False

    def __repr__(self):
        status = "已罚没(Slashed)" if self.is_slashed else "正常(Active)"
        return (f"验证者: {self.name:<8} | 质押量: {self.stake:>6.1f} 代币 | "
                f"出块数: {self.blocks_produced:>4} | 累计奖励: {self.rewards:>6.1f} | 状态: {status}")

class PoSConsensus:
    def __init__(self, block_reward: float = 2.0):
        self.validators: Dict[str, Validator] = {}
        self.block_reward = block_reward
        self.total_blocks = 0

    def add_validator(self, name: str, stake: float):
        """节点质押代币，加入验证者池"""
        if stake <= 0:
            raise ValueError("质押代币数必须大于 0")
        self.validators[name] = Validator(name, stake)

    def get_total_active_stake(self) -> float:
        """获取当前活跃（未被罚没）验证者的总质押代币数"""
        return sum(v.stake for v in self.validators.values() if not v.is_slashed)

    def select_proposer(self) -> Optional[Validator]:
        """根据节点质押金额占总质押池的比例，进行加权随机抽签选择出块人"""
        active_validators = [v for v in self.validators.values() if not v.is_slashed]
        total_stake = sum(v.stake for v in active_validators)

        if total_stake == 0 or not active_validators:
            return None

        # 加权随机选择 (Weighted Random Choice)
        pick = random.uniform(0, total_stake)
        current = 0.0
        for validator in active_validators:
            current += validator.stake
            if current >= pick:
                return validator
        return active_validators[-1]

    def produce_block(self) -> Optional[str]:
        """进行一轮出块：选择出块人并结算奖励"""
        proposer = self.select_proposer()
        if proposer is None:
            print("   [错误] 当前无可用活跃验证者，无法出块！")
            return None

        proposer.blocks_produced += 1
        proposer.rewards += self.block_reward
        proposer.stake += self.block_reward  # 奖励自动复利累加至质押池
        self.total_blocks += 1
        return proposer.name

    def slash(self, name: str, reason: str):
        """触发 Slashing 机制：扣除恶意验证者的质押金并踢出验证者列表"""
        validator = self.validators.get(name)
        if validator is None:
            print(f"   [错误] 未找到验证者 {name}")
            return

        if validator.is_slashed:
            print(f"   [提示] 验证者 {name} 已经被罚没过，无需重复处理")
            return

        print(f"\n   [安全警报 - 触发 Slashing] 验证者 '{name}' 严重违规！")
        print(f"   违规原因: {reason}")
        print(f"   惩罚决定: 没收全部质押资金 ({validator.stake:.1f} 代币) 并强制踢出验证者节点池！")

        validator.stake = 0.0
        validator.is_slashed = True

def main():
    # 设置随机数种子，保证实验输出可复现
    random.seed(42)

    print("==========================================")
    print("区块链 PoS (权益证明) 算法与 Slashing 惩罚实验")
    print("==========================================")

    pos = PoSConsensus(block_reward=2.0)

    # 1. 节点质押阶段
    print("\n1. 验证者节点质押代币加入权益池:")
    pos.add_validator("Alice", 500.0)
    pos.add_validator("Bob", 300.0)
    pos.add_validator("Charlie", 200.0)

    total_stake = pos.get_total_active_stake()
    print(f"   初始总质押量: {total_stake:.1f} 代币")
    print("   初始各节点权重分布:")
    for v in pos.validators.values():
        percentage = (v.stake / total_stake) * 100
        print(f"     - {v.name}: {v.stake:.1f} 代币 ({percentage:.1f}%)")

    # 2. 模拟 1000 轮 PoS 出块选举
    rounds = 1000
    print(f"\n2. 运行 {rounds} 轮 PoS 加权抽签出块选举:")
    for _ in range(rounds):
        pos.produce_block()

    print("\n   1000 轮出块后统计结果:")
    for v in pos.validators.values():
        actual_ratio = (v.blocks_produced / pos.total_blocks) * 100
        print(f"     - {v}")
        print(f"       实际出块占比: {actual_ratio:.2f}% (理论权重约为: {(v.stake / pos.get_total_active_stake()) * 100:.1f}%)")

    # 3. 模拟违规双签攻击并触发 Slashing 惩罚
    print("\n3. 模拟安全攻击测试 (Charlie 尝试在分叉链上进行双签 Double-Signing):")
    pos.slash("Charlie", reason="在同一区块高度恶意签署两条不同分叉链 (Double Signing Attack)")

    # 4. 展示 Slashing 后的验证者列表
    print("\n4. 触发 Slashing 后的验证者节点状态:")
    for v in pos.validators.values():
        print(f"   - {v}")

    # 5. 剔除违规节点后继续运行 100 轮
    new_rounds = 100
    print(f"\n5. 剔除违规节点后，继续运行 {new_rounds} 轮 PoS 出块:")
    for _ in range(new_rounds):
        pos.produce_block()

    print("\n   最新验证者列表与终态结算:")
    for v in pos.validators.values():
        print(f"   - {v}")

    print("\n==========================================")
    print("实验完成：成功验证了 PoS 权益加权出块与 Slashing 防双签惩罚！")
    print("==========================================")

if __name__ == "__main__":
    main()
