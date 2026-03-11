#!/usr/bin/env python3
import os
import sys
import json
import argparse
import subprocess
import datetime
from pathlib import Path

# 配置
BASE_DIR = Path(__file__).parent.resolve()
EXAMPLES_DIR = BASE_DIR / "examples"
LOGS_DIR = BASE_DIR / "logs"
REPORTS_DIR = BASE_DIR / "reports"

# 示例元数据
EXAMPLES = [
    {
        "name": "cmake_example",
        "display_name": "CMake示例集合",
        "category": "基础入门类",
        "description": "展示如何使用CMake将LiteRT集成到C++项目中",
        "language": "C++",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "cmake_example"
    },
    {
        "name": "minimal_tflite",
        "display_name": "最小化TFLite示例",
        "category": "基础入门类",
        "description": "最简单的C++示例，展示核心推理流程",
        "language": "C++",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "minimal_tflite"
    },
    {
        "name": "python_label_image",
        "display_name": "Python图像分类示例",
        "category": "基础入门类",
        "description": "Python版本的图像分类示例",
        "language": "Python",
        "run_script": "run.py",
        "working_dir": EXAMPLES_DIR / "python_label_image"
    },
    {
        "name": "cpp_label_image",
        "display_name": "C++图像分类工具",
        "category": "视觉AI应用类",
        "description": "功能完整的C++图像分类命令行工具",
        "language": "C++",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "cpp_label_image"
    },
    {
        "name": "web_depth_anything",
        "display_name": "深度估计Web Demo",
        "category": "视觉AI应用类",
        "description": "基于WebAssembly的单目深度估计在线演示",
        "language": "JavaScript",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "web_depth_anything"
    },
    {
        "name": "web_efficientvit_segmentation",
        "display_name": "图像分割Web Demo",
        "category": "视觉AI应用类",
        "description": "实时图像分割Web演示",
        "language": "JavaScript",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "web_efficientvit_segmentation"
    },
    {
        "name": "web_mobilenetv2",
        "display_name": "图像分类Web Demo",
        "category": "视觉AI应用类",
        "description": "图像分类Web演示",
        "language": "JavaScript",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "web_mobilenetv2"
    },
    {
        "name": "web_real_esrgan",
        "display_name": "超分辨率Web Demo",
        "category": "视觉AI应用类",
        "description": "基于Real-ESRGAN的图像超分辨率演示",
        "language": "JavaScript",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "web_real_esrgan"
    },
    {
        "name": "aot_backend_example",
        "display_name": "Python AOT后端示例",
        "category": "高级开发类",
        "description": "展示如何使用AOT提前编译功能",
        "language": "Python",
        "run_script": "run.py",
        "working_dir": EXAMPLES_DIR / "aot_backend_example"
    },
    {
        "name": "vendor_plugin_example",
        "display_name": "供应商插件开发示例",
        "category": "高级开发类",
        "description": "展示如何开发自定义算子插件",
        "language": "C++",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "vendor_plugin_example"
    },
    {
        "name": "stable_delegate_example",
        "display_name": "稳定委托API示例",
        "category": "高级开发类",
        "description": "展示如何使用稳定委托API接入硬件加速",
        "language": "C++",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "stable_delegate_example"
    },
    {
        "name": "converter_example",
        "display_name": "模型转换工具示例",
        "category": "高级开发类",
        "description": "展示如何使用模型转换器",
        "language": "Python",
        "run_script": "run.py",
        "working_dir": EXAMPLES_DIR / "converter_example"
    },
    {
        "name": "model_tools",
        "display_name": "模型工具套件",
        "category": "工具类",
        "description": "模型运行、分析、性能测试工具",
        "language": "C++/Python",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "model_tools"
    },
    {
        "name": "openvino_example",
        "display_name": "Intel OpenVINO配置示例",
        "category": "高级开发类",
        "description": "展示如何使用OpenVINO硬件加速",
        "language": "C++",
        "run_script": "run.sh",
        "working_dir": EXAMPLES_DIR / "openvino_example"
    }
]

def init_dirs():
    """初始化必要的目录"""
    LOGS_DIR.mkdir(exist_ok=True)
    REPORTS_DIR.mkdir(exist_ok=True)

def list_examples():
    """列出所有可用示例"""
    print("=" * 100)
    print(f"{'序号':<4} {'示例名称':<30} {'分类':<15} {'语言':<10} {'描述'}")
    print("=" * 100)
    for i, example in enumerate(EXAMPLES, 1):
        print(f"{i:<4} {example['display_name']:<30} {example['category']:<15} {example['language']:<10} {example['description']}")
    print("=" * 100)
    print(f"\n总共有 {len(EXAMPLES)} 个可用示例")

def get_example_by_name(name):
    """根据名称获取示例信息"""
    for example in EXAMPLES:
        if example["name"] == name:
            return example
    return None

def run_example(example, save_log=True):
    """运行单个示例"""
    print(f"\n{'='*60}")
    print(f"开始运行示例: {example['display_name']} ({example['name']})")
    print(f"{'='*60}")

    # 检查运行脚本是否存在
    run_script_path = example["working_dir"] / example["run_script"]
    if not run_script_path.exists():
        error_msg = f"错误: 运行脚本不存在: {run_script_path}"
        print(error_msg)
        return {
            "name": example["name"],
            "display_name": example["display_name"],
            "status": "failed",
            "error": error_msg,
            "duration": 0
        }

    # 构造命令
    if run_script_path.suffix == ".py":
        cmd = [sys.executable, str(run_script_path)]
    else:
        cmd = ["bash", str(run_script_path)]

    start_time = datetime.datetime.now()

    try:
        # 运行命令
        result = subprocess.run(
            cmd,
            cwd=str(example["working_dir"]),
            capture_output=True,
            text=True,
            timeout=300  # 5分钟超时
        )

        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()

        status = "success" if result.returncode == 0 else "failed"

        print(f"运行结果: {'✅ 成功' if status == 'success' else '❌ 失败'}")
        print(f"耗时: {duration:.2f} 秒")

        if result.returncode != 0:
            print(f"错误信息:\n{result.stderr}")

        # 保存日志
        if save_log:
            log_file = LOGS_DIR / f"{example['name']}_{start_time.strftime('%Y%m%d_%H%M%S')}.log"
            with open(log_file, "w") as f:
                f.write(f"=== 运行信息 ===\n")
                f.write(f"示例名称: {example['display_name']}\n")
                f.write(f"运行时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"运行命令: {' '.join(cmd)}\n")
                f.write(f"返回码: {result.returncode}\n")
                f.write(f"耗时: {duration:.2f} 秒\n\n")
                f.write(f"=== 标准输出 ===\n")
                f.write(result.stdout)
                f.write(f"\n=== 标准错误 ===\n")
                f.write(result.stderr)
            print(f"日志已保存到: {log_file}")

        return {
            "name": example["name"],
            "display_name": example["display_name"],
            "status": status,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "duration": duration
        }

    except subprocess.TimeoutExpired:
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        error_msg = "运行超时 (超过5分钟)"
        print(f"错误: {error_msg}")

        return {
            "name": example["name"],
            "display_name": example["display_name"],
            "status": "timeout",
            "error": error_msg,
            "duration": duration
        }
    except Exception as e:
        end_time = datetime.datetime.now()
        duration = (end_time - start_time).total_seconds()
        error_msg = f"运行异常: {str(e)}"
        print(f"错误: {error_msg}")

        return {
            "name": example["name"],
            "display_name": example["display_name"],
            "status": "error",
            "error": error_msg,
            "duration": duration
        }

def run_all_examples():
    """运行所有示例"""
    print(f"准备运行所有 {len(EXAMPLES)} 个示例...")

    results = []
    success_count = 0
    failed_count = 0
    timeout_count = 0
    error_count = 0

    for example in EXAMPLES:
        result = run_example(example)
        results.append(result)

        if result["status"] == "success":
            success_count += 1
        elif result["status"] == "failed":
            failed_count += 1
        elif result["status"] == "timeout":
            timeout_count += 1
        elif result["status"] == "error":
            error_count += 1

    # 输出汇总结果
    print("\n" + "=" * 80)
    print("运行汇总")
    print("=" * 80)
    print(f"总示例数: {len(EXAMPLES)}")
    print(f"成功: {success_count}")
    print(f"失败: {failed_count}")
    print(f"超时: {timeout_count}")
    print(f"异常: {error_count}")
    print(f"成功率: {success_count / len(EXAMPLES) * 100:.1f}%")

    # 保存结果
    result_file = REPORTS_DIR / f"run_all_results_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(result_file, "w") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f"\n完整结果已保存到: {result_file}")

    return results

def generate_report():
    """生成运行报告"""
    # 查找最新的运行结果文件
    result_files = sorted(REPORTS_DIR.glob("run_all_results_*.json"), reverse=True)
    if not result_files:
        print("错误: 没有找到运行结果文件，请先运行示例")
        return

    latest_result = result_files[0]
    with open(latest_result, "r") as f:
        results = json.load(f)

    # 统计信息
    total = len(results)
    success = sum(1 for r in results if r["status"] == "success")
    failed = sum(1 for r in results if r["status"] == "failed")
    timeout = sum(1 for r in results if r["status"] == "timeout")
    error = sum(1 for r in results if r["status"] == "error")
    avg_duration = sum(r["duration"] for r in results) / total if total > 0 else 0

    # 生成HTML报告
    html_content = f"""
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LiteRT 示例运行报告</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; font-family: Arial, sans-serif; }}
        body {{ padding: 20px; max-width: 1200px; margin: 0 auto; }}
        h1 {{ color: #2c3e50; margin-bottom: 20px; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-radius: 8px; margin-bottom: 20px; }}
        .summary-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-top: 15px; }}
        .summary-card {{ background: white; padding: 15px; border-radius: 6px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); text-align: center; }}
        .summary-card .number {{ font-size: 2em; font-weight: bold; margin-bottom: 5px; }}
        .success {{ color: #27ae60; }}
        .failed {{ color: #e74c3c; }}
        .timeout {{ color: #f39c12; }}
        .error {{ color: #9b59b6; }}
        table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        th, td {{ padding: 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background: #34495e; color: white; }}
        tr:hover {{ background: #f5f5f5; }}
        .status-badge {{ padding: 4px 8px; border-radius: 4px; color: white; font-size: 0.9em; }}
    </style>
</head>
<body>
    <h1>LiteRT 示例运行报告</h1>
    <p>生成时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p>结果文件: {latest_result.name}</p>

    <div class="summary">
        <h2>运行概览</h2>
        <div class="summary-grid">
            <div class="summary-card">
                <div class="number">{total}</div>
                <div>总示例数</div>
            </div>
            <div class="summary-card">
                <div class="number success">{success}</div>
                <div>成功</div>
            </div>
            <div class="summary-card">
                <div class="number failed">{failed}</div>
                <div>失败</div>
            </div>
            <div class="summary-card">
                <div class="number timeout">{timeout}</div>
                <div>超时</div>
            </div>
            <div class="summary-card">
                <div class="number error">{error}</div>
                <div>异常</div>
            </div>
            <div class="summary-card">
                <div class="number">{avg_duration:.2f}s</div>
                <div>平均耗时</div>
            </div>
        </div>
    </div>

    <h2>详细结果</h2>
    <table>
        <thead>
            <tr>
                <th>示例名称</th>
                <th>状态</th>
                <th>耗时(秒)</th>
            </tr>
        </thead>
        <tbody>
    """

    for result in results:
        status_class = {
            "success": "success",
            "failed": "failed",
            "timeout": "timeout",
            "error": "error"
        }.get(result["status"], "failed")

        status_text = {
            "success": "成功",
            "failed": "失败",
            "timeout": "超时",
            "error": "异常"
        }.get(result["status"], "未知")

        html_content += f"""
            <tr>
                <td>{result['display_name']}</td>
                <td><span class="status-badge {status_class}">{status_text}</span></td>
                <td>{result['duration']:.2f}</td>
            </tr>
        """

    html_content += """
        </tbody>
    </table>
</body>
</html>
    """

    report_file = REPORTS_DIR / f"run_report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    with open(report_file, "w") as f:
        f.write(html_content)

    print(f"报告已生成: {report_file}")
    print(f"可以在浏览器中打开查看详细结果")

def check_dependencies():
    """检查环境依赖"""
    print("正在检查环境依赖...\n")

    checks = [
        ("cmake --version", "CMake"),
        ("g++ --version", "GCC编译器"),
        ("python3 --version", "Python 3"),
        ("node --version", "Node.js"),
        ("npm --version", "NPM"),
    ]

    all_ok = True
    for cmd, name in checks:
        try:
            result = subprocess.run(cmd.split(), capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.splitlines()[0].strip()
                print(f"✅ {name}: {version}")
            else:
                print(f"❌ {name}: 未安装")
                all_ok = False
        except:
            print(f"❌ {name}: 未安装")
            all_ok = False

    # 检查Python包
    python_packages = ["numpy", "pillow", "tensorflow", "opencv-python"]
    print("\nPython 包检查:")
    for pkg in python_packages:
        try:
            result = subprocess.run([sys.executable, "-c", f"import {pkg.split('-')[0]}; print({pkg.split('-')[0]}.__version__)"],
                                  capture_output=True, text=True)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"✅ {pkg}: {version}")
            else:
                print(f"❌ {pkg}: 未安装")
                all_ok = False
        except:
            print(f"❌ {pkg}: 未安装")
            all_ok = False

    print("\n" + "=" * 50)
    if all_ok:
        print("✅ 所有依赖检查通过！")
    else:
        print("⚠️  部分依赖缺失，请安装后再运行示例")
    return all_ok

def main():
    init_dirs()

    parser = argparse.ArgumentParser(description="LiteRT 示例统一运行脚本")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # list 命令
    subparsers.add_parser("list", help="列出所有可用示例")

    # run 命令
    run_parser = subparsers.add_parser("run", help="运行指定示例")
    run_parser.add_argument("example_name", help="要运行的示例名称")

    # all 命令
    subparsers.add_parser("all", help="运行所有示例")

    # report 命令
    subparsers.add_parser("report", help="生成运行报告")

    # check 命令
    subparsers.add_parser("check", help="检查环境依赖")

    args = parser.parse_args()

    if args.command == "list":
        list_examples()
    elif args.command == "run":
        example = get_example_by_name(args.example_name)
        if not example:
            print(f"错误: 找不到示例 '{args.example_name}'，使用 list 命令查看所有可用示例")
            sys.exit(1)
        run_example(example)
    elif args.command == "all":
        check_dependencies()
        confirm = input("\n确认要运行所有示例吗？这可能需要较长时间 (y/N): ")
        if confirm.lower() == "y":
            run_all_examples()
        else:
            print("已取消运行")
    elif args.command == "report":
        generate_report()
    elif args.command == "check":
        check_dependencies()

if __name__ == "__main__":
    main()
