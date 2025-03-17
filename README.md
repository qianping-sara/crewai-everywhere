# Crew-AI 项目

这是一个基于 Crew AI 框架的智能代理系统项目，包含多个子项目用于不同的自动化任务。

## 项目结构

- `topic_research_crew/`: 主题研究智能代理
- `mail_crew/`: 邮件处理智能代理

## 环境要求

- Python 3.12
- 虚拟环境 (推荐)

## 安装说明

1. 克隆仓库：
```bash
git clone https://github.com/yourusername/crew-ai.git
cd crew-ai
```

2. 创建并激活虚拟环境：
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

3. 安装依赖：
```bash
pip install -r requirements.txt
```

## 使用方法

### Topic Research Crew

主题研究智能代理用于自动化研究特定主题并生成相关报告。

具体使用说明请参考 `topic_research_crew/` 目录下的文档。

### Mail Crew

邮件处理智能代理用于自动化邮件处理和回复。

具体使用说明请参考 `mail_crew/` 目录下的文档。

## 贡献指南

1. Fork 本仓库
2. 创建您的特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交您的更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启一个 Pull Request
