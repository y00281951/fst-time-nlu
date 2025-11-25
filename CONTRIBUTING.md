# 贡献指南

感谢您对 FST Time NLU 项目的关注！我们欢迎各种形式的贡献，包括但不限于：

- 报告 Bug
- 提交功能请求
- 改进文档
- 提交代码补丁
- 添加测试用例

## 行为准则

参与本项目即表示您同意遵守我们的行为准则。请保持友好、尊重和专业的态度。

## 如何报告 Bug

如果您发现了 Bug，请通过 GitHub Issues 报告，并包含以下信息：

1. **Bug 描述**：清晰简洁地描述问题
2. **复现步骤**：详细说明如何复现该问题
3. **预期行为**：描述您期望发生什么
4. **实际行为**：描述实际发生了什么
5. **环境信息**：
   - Python 版本
   - 操作系统
   - 相关依赖版本
6. **示例代码**：如果可能，提供最小可复现示例

## 如何提交功能请求

我们欢迎新功能建议！请通过 GitHub Issues 提交功能请求，并包含：

1. **功能描述**：清晰描述您希望添加的功能
2. **使用场景**：说明该功能的使用场景和价值
3. **可能的实现方案**：如果有想法，可以简要描述实现思路
4. **替代方案**：是否考虑过其他解决方案

## 开发环境设置

### 1. Fork 并克隆仓库

```bash
# Fork 项目到您的 GitHub 账号
# 然后克隆您的 fork
git clone https://github.com/YOUR_USERNAME/fst-time-nlu.git
cd fst-time-nlu
```

### 2. 创建虚拟环境

```bash
# 使用 venv
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
# 安装核心依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt

# 或者使用 pip install -e .[dev] 安装可编辑模式
pip install -e .[dev]
```

## 代码风格指南

本项目遵循 PEP 8 编码规范，并使用以下工具确保代码质量：

### 类型检查

使用 `mypy` 进行类型检查（可选）：

```bash
mypy src/
```

### 编码规范要点

1. **缩进**：使用 4 个空格
2. **行长度**：最大 100 字符
3. **命名规范**：
   - 类名：`PascalCase`
   - 函数/变量：`snake_case`
   - 常量：`UPPER_CASE`
4. **文档字符串**：使用三引号，遵循 Google 或 NumPy 风格
5. **导入顺序**：标准库 → 第三方库 → 本地模块
6. **类型注解**：建议为函数参数和返回值添加类型注解

## 提交 Pull Request 流程

### 1. 创建分支

```bash
# 从 main 分支创建新分支
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

分支命名规范：
- `feature/xxx`：新功能
- `fix/xxx`：Bug 修复
- `docs/xxx`：文档更新
- `refactor/xxx`：代码重构
- `test/xxx`：测试相关

### 2. 进行修改

- 编写代码
- 添加/更新测试
- 更新文档（如需要）
- 确保代码通过所有检查

### 3. 提交代码

```bash
# 添加修改的文件
git add .

# 提交（使用清晰的提交信息）
git commit -m "feat: 添加新功能描述"
```

提交信息格式（遵循 Conventional Commits）：
- `feat: 新功能`
- `fix: Bug 修复`
- `docs: 文档更新`
- `style: 代码格式调整`
- `refactor: 代码重构`
- `test: 测试相关`
- `chore: 构建/工具相关`

### 4. 推送到 GitHub

```bash
git push origin feature/your-feature-name
```

### 5. 创建 Pull Request

1. 访问您的 fork 仓库页面
2. 点击 "New Pull Request"
3. 填写 PR 标题和描述
4. 等待代码审查

### PR 描述模板

请在 PR 中包含以下信息：

- **变更类型**：功能/修复/文档/重构等
- **变更说明**：详细描述您的修改
- **相关 Issue**：如果有，请引用相关 Issue
- **测试**：说明如何测试您的修改
- **截图**：如果适用，提供截图

## 测试要求

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest src/english/test/test_english_time.py

# 运行并查看覆盖率
pytest --cov=src --cov-report=html
```

### 编写测试

- 为新功能添加测试用例
- 确保测试覆盖率不降低
- 测试文件命名：`test_*.py` 或 `*_test.py`
- 测试函数命名：`test_*`

示例：

```python
def test_parse_chinese_time():
    """测试中文时间解析"""
    extractor = FstTimeExtractor()
    result = extractor.extract("明天上午9点")
    assert len(result) > 0
```

## 文档贡献

文档改进同样重要！您可以：

- 修正拼写/语法错误
- 改进现有文档的清晰度
- 添加使用示例
- 翻译文档

文档位置：
- 主文档：`README.md`

## 代码审查

所有 PR 都需要经过代码审查。审查者会关注：

1. **代码质量**：是否遵循编码规范
2. **功能正确性**：是否实现了预期功能
3. **测试覆盖**：是否有足够的测试
4. **文档完整性**：是否更新了相关文档
5. **向后兼容性**：是否破坏了现有 API

请耐心等待审查，并根据反馈进行修改。

## 发布流程

项目维护者负责版本发布。发布流程：

1. 更新 `CHANGELOG.md`
2. 更新版本号（`pyproject.toml`）
3. 创建 Git tag
4. 发布到 PyPI（如适用）

## 获取帮助

如果您在贡献过程中遇到问题：

1. 查看现有 Issues 和 PR
2. 阅读项目文档
3. 在 Issue 中提问
4. 联系维护者：
   - Ming Yu: yuming@oppo.com
   - Liangliang Han: hanliangliang@oppo.com

## 许可证

通过向本项目提交代码，您同意您的贡献将在 Apache License 2.0 下授权。

---

再次感谢您的贡献！🎉

