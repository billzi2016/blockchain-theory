#!/bin/bash

# 设置终端编码为 UTF-8
export LANG=C.UTF-8
export LC_ALL=C.UTF-8

# 进入脚本所在目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

echo "=================================================="
echo "启动时间: $(date '+%Y-%m-%d %H:%M:%S')"
echo "工作目录: $SCRIPT_DIR"
echo "正在以 Release 模式编译并运行 Rust PoW Hash 扫描器..."
echo "=================================================="

# 使用 tee 保留命令行控制台完整输出到 console.log
cargo run --release 2>&1 | tee -a console.log
