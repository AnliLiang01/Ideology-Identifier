# Ideology-Identifier
Gender/Political Ideology Identifier for Chinese Social Media Texts

# 当前版本为本地运行的demo，含后端+前端展示。先进行本地运行测试，该版本的效果无大问题后可再进行Flask部署

# demo本地运行指南：
1. 准备本地目录结构:
2.
```
your_project/
├── app.py
└── templates/
    └── index.html
```
3. 更新python为大于3.9版本
4. 安装依赖
  `pip install flask transformers beautifulsoup4 requests`

5. 运行
   `python app.py`
6. 访问浏览器打开：http://localhost:5000
   就可以输入中文或支持的网页链接，测试分析功能。
