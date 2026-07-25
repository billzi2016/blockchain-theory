import hashlib
import os

# Secp256k1 椭圆曲线参数 (比特币标准)
P = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEFFFFFC2F
A = 0
B = 7
Gx = 0x79BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798
Gy = 0x483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8
G = (Gx, Gy)
N = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

def mod_inverse(k: int, p: int = P) -> int:
    """扩展欧几里得算法计算模逆元"""
    if k == 0:
        raise ZeroDivisionError("除数不能为 0")
    if k < 0:
        return p - mod_inverse(-k, p)
    s, old_s = 0, 1
    t, old_t = 1, 0
    r, old_r = p, k
    while r != 0:
        quotient = old_r // r
        old_r, r = r, old_r - quotient * r
        old_s, s = s, old_s - quotient * s
        old_t, t = t, old_t - quotient * t
    return old_s % p

def point_add(p1, p2):
    """椭圆曲线点加法 P1 + P2"""
    if p1 is None:
        return p2
    if p2 is None:
        return p1

    x1, y1 = p1
    x2, y2 = p2

    if x1 == x2 and y1 != y2:
        return None

    if x1 == x2:
        # 点倍运算 (P1 == P2)
        m = (3 * x1 * x1 + A) * mod_inverse(2 * y1, P) % P
    else:
        m = (y2 - y1) * mod_inverse(x2 - x1, P) % P

    x3 = (m * m - x1 - x2) % P
    y3 = (m * (x1 - x3) - y1) % P
    return (x3, y3)

def point_multiply(k: int, point=G):
    """椭圆曲线标量乘法 k * Point"""
    result = None
    addend = point
    while k:
        if k & 1:
            result = point_add(result, addend)
        addend = point_add(addend, addend)
        k >>= 1
    return result

def generate_keypair():
    """生成私钥与公钥对"""
    # 随机选择私钥 d 属于 [1, N-1]
    private_key = int.from_bytes(os.urandom(32), 'big') % (N - 1) + 1
    public_key = point_multiply(private_key, G)
    return private_key, public_key

def get_address(public_key) -> str:
    """根据公钥计算模拟地址 (SHA256)"""
    pub_bytes = f"{public_key[0]:064x}{public_key[1]:064x}".encode('utf-8')
    return hashlib.sha256(pub_bytes).hexdigest()[:40]

def sign(private_key: int, message: str):
    """使用私钥对消息签名，返回 (r, s)"""
    z = int.from_bytes(hashlib.sha256(message.encode('utf-8')).digest(), 'big')
    r, s = 0, 0
    while r == 0 or s == 0:
        k = int.from_bytes(os.urandom(32), 'big') % (N - 1) + 1
        kg = point_multiply(k, G)
        r = kg[0] % N
        if r == 0:
            continue
        k_inv = mod_inverse(k, N)
        s = (k_inv * (z + r * private_key)) % N
    return (r, s)

def verify(public_key, message: str, signature) -> bool:
    """使用公钥验证消息签名 (r, s)"""
    r, s = signature
    if not (1 <= r < N and 1 <= s < N):
        return False
    z = int.from_bytes(hashlib.sha256(message.encode('utf-8')).digest(), 'big')
    w = mod_inverse(s, N)
    u1 = (z * w) % N
    u2 = (r * w) % N
    p1 = point_multiply(u1, G)
    p2 = point_multiply(u2, public_key)
    point = point_add(p1, p2)
    if point is None:
        return False
    return (point[0] % N) == r

def main():
    print("==========================================")
    print("比特币 Secp256k1 椭圆曲线数字签名实验程序")
    print("==========================================")

    # 1. 密钥对生成
    private_key, public_key = generate_keypair()
    address = get_address(public_key)

    print(f"\n1. 成功生成 Secp256k1 密钥对与地址:")
    print(f"   私钥 (Private Key): 0x{private_key:064x}")
    print(f"   公钥 X 坐标: 0x{public_key[0]:064x}")
    print(f"   公钥 Y 坐标: 0x{public_key[1]:064x}")
    print(f"   导出比特币模拟地址: {address}")

    # 2. 消息签名测试
    message = "Alice 授权支付 5 BTC 给 Bob"
    print(f"\n2. 待签名的原始交易消息:")
    print(f"   Message: '{message}'")

    r, s = sign(private_key, message)
    print(f"\n3. 私钥签名成功，生成 ECDSA 签名 (r, s):")
    print(f"   r: 0x{r:064x}")
    print(f"   s: 0x{s:064x}")

    # 3. 验证签名 (合法情况)
    is_valid = verify(public_key, message, (r, s))
    print(f"\n4. 使用公钥进行签名合法性验证:")
    print(f"   验证结果: {is_valid}")

    # 4. 防篡改测试：消息被修改
    tampered_message = "Alice 授权支付 500 BTC 给 Bob"
    is_tampered_valid = verify(public_key, tampered_message, (r, s))
    print(f"\n5. 验证交易防篡改拦截 (攻击者修改转账金额为 500 BTC):")
    print(f"   验证结果: {is_tampered_valid}")

    # 5. 防伪造测试：用假私钥生成的伪造签名
    fake_priv, _ = generate_keypair()
    fake_r, fake_s = sign(fake_priv, message)
    is_fake_valid = verify(public_key, message, (fake_r, fake_s))
    print(f"\n6. 验证冒充身份拦截 (黑客用别人的公钥验证自己的签名):")
    print(f"   验证结果: {is_fake_valid}")
    print("==========================================")

if __name__ == "__main__":
    main()
