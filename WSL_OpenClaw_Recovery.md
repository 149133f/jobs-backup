# WSL OpenClaw 緊急復原指南

## 📋 系統架構

| 系統 | Agent | Port | 用途 |
|------|-------|------|------|
| **WSL** | 小喬 (主程式) | 18789 | 主要對話 |
| **WSL** | Jobs (技術擔當) | 18789 | 技術協助 |
| **Windows** | Jarvis | 18790 | 管家 |

> ⚠️ 小喬和 Jobs 共用同一個 OpenClaw Gateway (Port 18789)

---

## 🚀 快速復原

### 方法 1：SSH + Git Clone（推薦）

```bash
# 1. 進入 WSL
wsl -d Ubuntu

# 2. 導航到工作目錄
cd /home/feng/.openclaw/

# 3. Clone 倉庫
git clone https://github.com/149133f/jobs-backup.git workspace-jobs

# 4. Clone 小喬備份
git clone git@github.com:149133f/piggy-backup.git workspace
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

### 步驟 3：設定 Git SSH Key

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

### 步驟 4：Clone 所有備份

```bash
cd /home/feng/.openclaw/

# 小喬的備份
git clone git@github.com:149133f/piggy-backup.git workspace

# Jobs 的備份
git clone git@github.com:149133f/jobs-backup.git workspace-jobs
```

### 步驟 5：驗證核心檔案

```bash
# 小喬
ls -la /home/feng/.openclaw/workspace/SOUL.md AGENTS.md USER.md

# Jobs
ls -la /home/feng/.openclaw/workspace-jobs/SOUL.md AGENTS.md USER.md
```

### 步驟 6：啟動 OpenClaw Gateway

```bash
# 在 WSL 執行
openclaw gateway start
```

### 步驟 7：驗證狀態

```bash
curl http://127.0.0.1:18789/health
```

---

## 📁 重要檔案清單

### 小喬 (workspace/)

| 檔案 | 用途 |
|------|------|
| `SOUL.md` | 小喬的靈魂設定 |
| `AGENTS.md` | Agent 設定 |
| `USER.md` | 用戶設定 |
| `MEMORY.md` | 長期記憶 |
| `HEARTBEAT.md` | 心跳檢查設定 |
| `IDENTITY.md` | 身份設定 |
| `memory/` | 每日記憶 |

### Jobs (workspace-jobs/)

| 檔案 | 用途 |
|------|------|
| `SOUL.md` | Jobs 的靈魂設定 |
| `AGENTS.md` | Agent 設定 |
| `USER.md` | 用戶設定 |
| `JOBS_SAFETY.md` | 安全規範 |
| `memory/` | 每日記憶 |

---

## 🔄 日常備份

```bash
# 備份小喬
cd /home/feng/.openclaw/workspace
git add -A
git commit -m "Backup $(date '+%Y-%m-%d %H:%M')"
git push origin master

# 備份 Jobs
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

### Q: 小喬/Jobs 沒有回應？
**A:** 檢查 Gateway 狀態

```bash
curl http://127.0.0.1:18789/health
```

### Q: Port 18789 被佔用？
```bash
ss -tlnp | grep 18789
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
   git clone git@github.com:149133f/piggy-backup.git workspace
   git clone git@github.com:149133f/jobs-backup.git workspace-jobs
   ```

4. **啟動 Gateway**
   ```bash
   openclaw gateway start
   ```

---

## 📞 GitHub 倉庫

| 倉庫 | 連結 |
|------|------|
| 小喬 | https://github.com/149133f/piggy-backup |
| Jobs | https://github.com/149133f/jobs-backup |
| Jarvis | https://github.com/149133f/jarvis-backup |

---

如有問題，請聯繫師父！
