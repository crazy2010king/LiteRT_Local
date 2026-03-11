# LiteRT 示例程序集合

本目录包含了LiteRT框架的各类示例程序，方便开发者快速学习和使用LiteRT的各种功能。

## 快速开始

### 1. 环境配置
首先安装必要的依赖：
```bash
# 安装系统依赖
sudo apt update && sudo apt install -y build-essential cmake git python3 python3-pip nodejs npm

# 安装Python依赖
pip3 install numpy pillow tensorflow opencv-python

# 安装Node.js依赖
npm install -g http-server
```

### 2. 查看所有示例
```bash
python run_all_examples.py list
```

### 3. 运行指定示例
```bash
python run_all_examples.py run minimal_tflite
```

### 4. 运行所有示例
```bash
python run_all_examples.py all
```

### 5. 查看运行报告
```bash
python run_all_examples.py report
```

## 目录结构
```
├── litert_examples_guide.md    # 详细的使用指南（5000+字）
├── README.md                   # 本快速开始文件
├── run_all_examples.py         # 统一运行脚本
├── examples/                   # 所有示例程序目录
│   ├── cmake_example/          # CMake集成示例
│   ├── minimal_tflite/         # 最小化C++示例
│   ├── python_label_image/     # Python图像分类示例
│   ├── cpp_label_image/        # C++图像分类工具
│   ├── web_depth_anything/     # 深度估计Web Demo
│   ├── web_efficientvit_segmentation/ # 图像分割Web Demo
│   ├── web_mobilenetv2/        # 图像分类Web Demo
│   ├── web_real_esrgan/        # 超分辨率Web Demo
│   ├── aot_backend_example/    # Python AOT后端示例
│   ├── vendor_plugin_example/  # 供应商插件开发示例
│   ├── stable_delegate_example/ # 稳定委托API示例
│   ├── converter_example/      # 模型转换工具示例
│   ├── model_tools/            # 模型工具套件
│   └── openvino_example/       # Intel OpenVINO加速示例
├── logs/                       # 运行日志存储目录
└── reports/                    # 运行报告存储目录
```

## 文档说明
详细的使用教程、原理说明、最佳实践请查看 `litert_examples_guide.md` 文件，包含：
- 框架概述与核心架构
- 环境配置与编译教程
- 每个示例的详细使用说明
- 性能优化技巧与常见问题解答
- 统一运行脚本的完整功能说明

## 支持状态
本示例集合已在以下环境测试通过：
- ✅ Ubuntu 22.04.4 LTS x86_64
- ✅ Intel Core i7-14700K CPU
- ✅ Python 3.10.12
- ✅ CMake 3.22.1
- ✅ Node.js 25.7.0

## 相关资源
- [LiteRT开源项目仓库](https://github.com/crazy2010king/LiteRT_Local)
- [TensorFlow Lite官方文档](https://www.tensorflow.org/lite/guide)
- [示例程序详细使用指南](./litert_examples_guide.md)
