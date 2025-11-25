# Streamlit Cloud 部署指南

本应用已部署到 Streamlit Cloud，用户可以直接访问在线演示。

## 🌐 在线演示

**访问地址**：https://fst-time-nlu-t52oauj46kezvmgah25whe.streamlit.app/

## 🚀 如何部署自己的实例

### 步骤 1：Fork 项目

1. 访问 https://github.com/y00281951/fst-time-nlu
2. 点击右上角 "Fork" 按钮

### 步骤 2：部署到 Streamlit Cloud

1. 访问 https://share.streamlit.io/
2. 使用 GitHub 账号登录
3. 点击 "New app"
4. 填写信息：
   ```
   Repository: your-username/fst-time-nlu
   Branch: main
   Main file path: app.py
   ```
5. 点击 "Deploy!"
6. 等待 3-5 分钟完成部署

### 步骤 3：获取应用 URL

部署成功后，你会获得类似这样的 URL：
```
https://your-app-name.streamlit.app
```

## 📦 依赖文件

应用会自动检测并安装以下依赖：

### Python 依赖 (`requirements.txt`)
```txt
streamlit>=1.28.0
pynini>=2.1.5
python-dateutil>=2.8.0
zhdate
lunarcalendar
inflect>=5.0.0
PyYAML>=5.0.0
importlib-resources>=5.0.0
```

### 系统依赖 (`packages.txt`)
```txt
libfst-dev
libfst-tools
```

### Streamlit 配置 (`.streamlit/config.toml`)
```toml
[server]
port = 8501
headless = true
enableCORS = false

[browser]
gatherUsageStats = false

[theme]
primaryColor = "#1f77b4"
backgroundColor = "#ffffff"
secondaryBackgroundColor = "#f0f2f6"
textColor = "#262730"
```

## 🔄 自动更新

每次推送代码到 GitHub，Streamlit Cloud 会自动重新部署：

```bash
git add .
git commit -m "update: 优化功能"
git push origin main
# 等待 1-2 分钟，应用自动更新
```

## ⚙️ 配置选项

### Advanced Settings

部署时可以点击 "Advanced settings" 配置：

- **Python version**: 建议 `3.9` 或更高
- **Secrets**: 本应用不需要环境变量

## 🐛 故障排查

### 问题 1：ModuleNotFoundError

**解决**：确保 `requirements.txt` 包含所有依赖

### 问题 2：pynini 编译失败

**解决**：确保 `packages.txt` 包含：
```txt
libfst-dev
libfst-tools
```

### 问题 3：应用休眠

**说明**：免费版应用在 7 天无访问后会休眠，首次访问需要 10-30 秒唤醒。

## 📚 更多资源

- [Streamlit 官方文档](https://docs.streamlit.io/)
- [Streamlit Cloud 部署指南](https://docs.streamlit.io/streamlit-community-cloud)
- [项目 GitHub](https://github.com/y00281951/fst-time-nlu)

---

**问题反馈**：https://github.com/y00281951/fst-time-nlu/issues

