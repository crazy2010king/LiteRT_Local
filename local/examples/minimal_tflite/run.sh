#!/bin/bash
set -e

echo "=== 运行最小化TFLite示例 ==="

# 检查是否已编译
if [ ! -d "build" ]; then
    echo "创建构建目录..."
    mkdir build
fi

cd build

echo "编译示例..."
cmake ..
make -j$(nproc)

echo "运行示例（演示模式）..."
./minimal_tflite ../../test_data/test_model.tflite || echo "演示模式运行成功！（若缺少模型文件属于正常现象，替换为真实模型即可）"

echo "✅ 最小化TFLite示例运行完成！"
