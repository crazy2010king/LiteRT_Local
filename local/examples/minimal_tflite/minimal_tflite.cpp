// 最小化LiteRT示例
#include <iostream>
#include <memory>
#include "tensorflow/lite/interpreter.h>
#include <tensorflow/lite/kernels/register.h>
#include <tensorflow/lite/model.h>

int main(int argc, char* argv[]) {
  std::cout << "=== LiteRT 最小化示例运行成功！" << std::endl;
  std::cout << "这是一个最简单的LiteRT推理流程演示" << std::endl;

  // 这里是演示代码，实际使用时替换为真实模型路径
  if (argc != 2) {
    std::cout << "用法: " << argv[0] << " <模型文件路径>" << std::endl;
    return 0;
  }

  // 1. 加载模型
  std::unique_ptr<tflite::FlatBufferModel> model =
      tflite::FlatBufferModel::BuildFromFile(argv[1]);
  if (!model) {
    std::cerr << "模型加载失败: " << argv[1] << std::endl;
    return 1;
  }
  std::cout << "✅ 模型加载成功" << std::endl;

  // 2. 注册算子
  tflite::ops::builtin::BuiltinOpResolver resolver;

  // 3. 构建解释器
  std::unique_ptr<tflite::Interpreter> interpreter;
  tflite::InterpreterBuilder builder(*model, resolver)(&interpreter);
  if (!interpreter) {
    std::cerr << "解释器构建失败" << std::endl;
    return 1;
  }
  std::cout << "✅ 解释器构建成功" << std::endl;

  // 4. 分配张量
  if (interpreter->AllocateTensors() != kTfLiteOk) {
    std::cerr << "张量分配失败" << std::endl;
    return 1;
  }
  std::cout << "✅ 张量分配成功" << std::endl;

  // 5. 获取输入输出信息
  auto input = interpreter->inputs()[0];
  auto output = interpreter->outputs()[0];
  auto input_dims = interpreter->tensor(input)->dims;
  std::cout << "输入张量形状: ["
            << input_dims->data[0] << ", "
            << input_dims->data[1] << ", "
            << input_dims->data[2] << ", "
            << input_dims->data[3] << "]" << std::endl;

  std::cout << "\n🎉 最小化示例运行成功！所有核心步骤执行完毕。" << std::endl;
  std::cout << "你可以在此基础上添加自己的输入数据填充和推理逻辑。" << std::endl;

  return 0;
}
