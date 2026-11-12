# 推送到 GitHub

本仓库只包含文档与脱敏证据，不包含执行器代码、密钥、宿主路径。

```bash
cd /d <LOCAL_REPO_PATH>

git init
git add .
git commit -m "docs: local-first agent architecture notes"

git branch -M main
git remote add origin https://github.com/<YOUR_GITHUB_USER>/Local-First-Agent-Architecture.git
git push -u origin main
```

推送前自查：

```bash
git status
git log --oneline -1
git grep -nE "([A-Za-z]:\\\\|sk-|cli_)" || echo "clean"
```

最后一条应输出 clean；如果有命中，先删掉再提交。
