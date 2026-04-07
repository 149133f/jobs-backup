# Jobs 緊急復原指南 - 賈伯斯 (Jobs)

## 📋 基本資料

| 項目 | 內容 |
|------|------|
| **名稱** | Jobs (賈伯斯) |
| **系統** | WSL (Windows Subsystem for Linux) |
| **Port** | 18789 |
| **CDP Port** | 9224 |
| **角色** | 技術擔當 |
| **Repository** | https://github.com/149133f/jobs-backup |

---

## 🚀 快速復原

### 方法 1：SSH + Git Clone（推薦）

```bash
# 1. 進入 WSL
wsl -d Ubuntu

# 2. 導航到工作目錄
cd /home/feng/.openclaw/

# 3. Clone 倉庫（如果需要）
git clone https://github.com/149133f/jobs-backup.git workspace-jobs

# 4. 進入 Jobs 工作區
cd workspace-jobs

# 5. 驗證重要檔案
ls -la SOUL.md AGENTS.md USER.md MEMORY.md
```

### 方法 2：手動下載 ZIP

1. 前往 https://github.com/149133f/jobs-backup
2. 點擊 **Code** → **Download ZIP**
3. 解壓縮到 `/home/feng/.openclaw/workspace-jobs/`

---

## 🔧 完整復原步驟

### 步驟 1：確認 WSL 正常

```powershell
# 在 Windows CMD
wsl --status
wsl -d Ubuntu
```

### 步驟 2：確認 OpenClaw 已安裝

```bash
which openclaw
openclaw --version
```

如果沒有，執行：
```bash
npm install -g openclaw
```

### 步驟 3：設定 Git SSH Key（用於未來備份）

```bash
# 產生 SSH Key
ssh-keygen -t ed25519 -C "jobs@openclaw.ai" -f ~/.ssh/id_ed25519 -N ""

# 複製公鑰
cat ~/.ssh/id_ed25519.pub
```

**把公鑰加到 GitHub：**
1. 登入 https://github.com/settings/keys
2. 點擊 **New SSH key**
3. 貼上公鑰

### 步驟 4：Clone 或更新備份

```bash
cd /home/feng/.openclaw/

# 如果是新的
git clone git@github.com:149133f/jobs-backup.git workspace-jobs

# 如果已存在，更新
cd workspace-jobs
git pull origin main
```

### 步驟 5：驗證核心檔案

```bash
cd /home/feng/.openclaw/workspace-jobs/
ls -la SOUL.md AGENTS.md USER.md MEMORY.md JOBS_SAFETY.md
```

### 步驟 6：啟動 Jobs

```bash
# 在 WSL 執行
openclaw agents add jobs
openclaw gateway restart
```

---

## 📁 重要檔案清單

| 檔案 | 用途 |
|------|------|
| `SOUL.md` | Jobs 的靈魂設定 |
| `AGENTS.md` | Agent 設定 |
| `USER.md` | 用戶設定 |
| `MEMORY.md` | 長期記憶 |
| `JOBS_SAFETY.md` | 安全規範 |
| `memory/` | 每日記憶 |
| `scripts/` | 腳本檔案 |
| `skills/` | 技能檔案 |

---

## 🔄 日常備份（用 SSH）

```bash
cd /home/feng/.openclaw/workspace-jobs
git add -A
git commit -m "Backup $(date '+%Y-%m-%d %H:%M')"
git push origin main
```

---

## ⚠️ 常見問題

### Q: Git Push 失敗？
**A:** 確認 SSH Key 已加到 GitHub

```bash
ssh -T git@github.com
# 應該顯示：Hi 149133f! You've successfully authenticated.
```

### Q: OpenClaw 無法啟動？
**A:** 檢查 Port 是否被佔用

```bash
ss -tlnp | grep 18789
```

### Q: Chrome CDP 無法連接？
**A:** 確認 Chrome 已啟動

```bash
# 在 WSL
bash /home/feng/.openclaw/workspace/scripts/start-chrome.sh
```

---

## 🆘 緊急救援

如果完全損壞：

1. **重啟 WSL**
   ```powershell
   wsl --shutdown
   wsl -d Ubuntu
   ```

2. **重新安裝 OpenClaw**
   ```bash
   npm install -g openclaw
   ```

3. **Clone 最新備份**
   ```bash
   cd /home/feng/.openclaw/
   git clone git@github.com:149133f/jobs-backup.git workspace-jobs
   ```

4. **設定並啟動**
   ```bash
   openclaw agents add jobs
   openclaw gateway start
   ```

---

## 📞 聯繫

如有問題，請聯繫師父！
