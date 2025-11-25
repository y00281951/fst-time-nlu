---
name: Bug 报告
about: 报告一个问题以帮助我们改进
title: '[BUG] '
labels: bug
assignees: ''

---

## Bug 描述
清晰简洁地描述这个 Bug。

## 复现步骤
详细说明如何复现该问题：

1. 执行 '...'
2. 输入 '...'
3. 查看 '...'
4. 出现错误

## 预期行为
清晰简洁地描述您期望发生什么。

## 实际行为
清晰简洁地描述实际发生了什么。

## 最小可复现示例
如果可能，请提供最小可复现代码：

```python
from src.chinese.fst_time_extractor import FstTimeExtractor

extractor = FstTimeExtractor()
result = extractor.extract("您的测试文本")
print(result)
```

## 环境信息
请提供以下信息：

- **操作系统**：[例如：Ubuntu 20.04, Windows 10, macOS 12.0]
- **Python 版本**：[例如：3.8.10]
- **fst-time-nlu 版本**：[例如：0.1.0]
- **相关依赖版本**：
  - pynini: [版本号]
  - 其他相关依赖

获取版本信息：
```bash
python --version
pip show fst-time-nlu
pip show pynini
```

## 错误信息
如果有错误信息或堆栈跟踪，请粘贴在这里：

```
粘贴完整的错误信息
```

## 截图
如果适用，请添加截图以帮助解释问题。

## 附加信息
添加任何其他有关该问题的信息。

## 可能的解决方案
如果您有任何关于如何修复此问题的想法，请在此处描述。

