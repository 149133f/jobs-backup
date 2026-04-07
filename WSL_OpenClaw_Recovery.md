# WSL OpenClaw 緊急復原指南

## 📋 系統架構

| 系統 | Agent | Port | 用途 |
|------|-------|------|------|
| **WSL** | 小喬 (主程式) | 18789 | 主要對話 |
| **WSL** | Jobs (技術擔當) | 18789 | 技術協助 |
| **Windows** | Jarvis | 18790 | 管家 |

> ⚠️ 小喬和 Jobs 共用同一個 OpenClaw Gateway (Port 18789)
> ⚠️ 重要：Jobs 是 WSL 版，運行於 `/home/feng/.openclaw/workspace-jobs/`

---

## 🚀 快速復原（只需 6 步）

```bash
# 步驟 1：進入 WSL
wsl -d Ubuntu

# 步驟 2：Clone 所有備份
cd /home/feng/.openclaw/
git clone git@github.com:149133f/jobs-backup.git workspace-jobs
git clone git@github.com:149133f/piggy-backup.git workspace

# 步驟 3：設定 Git SSH Key（如沒有）
ssh-keygen -t ed25519 -C "jobs@openclaw.ai" -f ~/.ssh/id_ed25519 -N ""
# 複製公鑰並加到 GitHub

# 步驟 4：確認 OpenClaw 已安裝
npm install -g openclaw

# 步驟 5：啟動 Gateway
openclaw gateway start

# 步驟 6：驗證狀態
curl http://127.0.0.1:18789/health
```

---

## 🔧 詳細復原步驟

### 步驟 1：進入 WSL

在 Windows CMD 或 PowerShell 執行：
```powershell
wsl -d Ubuntu
```

### 步驟 2：安裝 OpenClaw（如需要）

```bash
# 安裝
npm install -g openclaw

# 驗證
openclaw --version
```

### 步驟 3：Clone 備份

```bash
cd /home/feng/.openclaw/

# Clone 小喬的備份
git clone git@github.com:149133f/piggy-backup.git workspace

# Clone Jobs 的備份
git clone git@github.com:149133f/jobs-backup.git workspace-jobs
```

### 步驟 4：設定 SSH Key（如沒有）

```bash
# 產生 SSH Key
ssh-keygen -t ed25519 -C "jobs@openclaw.ai" -f ~/.ssh/id_ed25519 -N ""

# 複製公鑰
cat ~/.ssh/id_ed25519.pub
```

**把公鑰加到 GitHub：**
1. 前往 https://github.com/settings/keys
2. 點擊 **New SSH key**
3. 貼上公鑰

### 步驟 5：驗證目錄結構

```bash
# 確認目錄存在
ls -la /home/feng/.openclaw/workspace/
ls -la /home/feng/.openclaw/workspace-jobs/

# 確認核心檔案
ls /home/feng/.openclaw/workspace/SOUL.md
ls /home/feng/.openclaw/workspace-jobs/SOUL.md
```

### 步驟 6：啟動 OpenClaw Gateway

```bash
# 方法 A：使用系統服务
systemctl --user start openclaw-gateway.service

# 方法 B：直接啟動
openclaw gateway start
```

### 步驟 7：驗證狀態

```bash
# 檢查健康狀態
curl http://127.0.0.1:18789/health

# 應該回應：{"status":"ok"}

# 檢查 Agent 狀態
openclaw status
```

### 步驟 8：重啟 Gateway（如需要）

```bash
openclaw gateway restart
```

---

## 📁 必須備份的檔案

### 小喬 (workspace/)

```
workspace/
├── SOUL.md              # ⭐ 靈魂設定（最重要）
├── AGENTS.md            # ⭐ Agent 設定
├── USER.md              # ⭐ 用戶設定
├── MEMORY.md            # ⭐ 長期記憶
├── HEARTBEAT.md         # 心跳檢查
├── IDENTITY.md          # 身份設定
├── TOOLS.md            # 工具設定
├── RECOVERY.md         # 復原指南
├── WSL_OpenClaw_Recovery.md  # 統一復原指南
├── memory/             # ⭐ 每日記憶
│   ├── 2026-*.md
│   └── heartbeat-state.json
├── skills/             # 技能設定
├── scripts/           # 腳本
└── .openclaw/         # OpenClaw 設定
    └── workspace-state.json
```

### Jobs (workspace-jobs/)

```
workspace-jobs/
├── SOUL.md              # ⭐ 靈魂設定（最重要）
├── AGENTS.md            # ⭐ Agent 設定
├── USER.md              # ⭐ 用戶設定
├── MEMORY.md            # ⭐ 長期記憶
├── JOBS_SAFETY.md       # ⭐ 安全規範
├── HEARTBEAT.md         # 心跳檢查
├── IDENTITY.md          # 身份設定
├── TOOLS.md            # 工具設定
├── RECOVERY.md         # 復原指南
├── WSL_OpenClaw_Recovery.md  # 統一復原指南
├── memory/             # ⭐ 每日記憶
│   └── 2026-*.md
├── scripts/            # 腳本
├── skills/             # 技能
├── .clawhub/          # ClawHub 設定
└── .openclaw/         # OpenClaw 設定
    └── workspace-state.json
```

---

## 🔄 日常備份（每次更動後執行）

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

### Q1: Git Push 失敗？
```bash
# 確認 SSH Key
ssh -T git@github.com
# 應該顯示：Hi 149133f! You've successfully authenticated.

# 如果失敗，產生新的 SSH Key
ssh-keygen -t ed25519 -C "jobs@openclaw.ai" -f ~/.ssh/id_ed25519 -N ""
```

### Q2: Port 18789 被佔用？
```bash
# 檢查
ss -tlnp | grep 18789

# 殺掉佔用的程式
kill <PID>
```

### Q3: 小喬/Jobs 沒有回應？
```bash
# 檢查 Gateway 狀態
curl http://127.0.0.1:18789/health

# 重啟 Gateway
openclaw gateway restart
```

### Q4: npm 安裝失敗？
```bash
# 使用 sudo
sudo npm install -g openclaw

# 或修復權限
mkdir -p ~/.npm-global
npm config set prefix '~/.npm-global'
echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

---

## 🆘 緊急救援（完全損壞時）

### 情況 1：WSL 完全損壞

1. **重啟 WSL**
   ```powershell
   wsl --shutdown
   wsl -d Ubuntu
   ```

2. **檢查 WSL 狀態**
   ```powershell
   wsl --status
   wsl --list -v
   ```

3. **如需重新安裝 WSL**
   - 參考 Windows 功能：啟用「適用於 Linux 的 Windows 子系統」
   - 從 Microsoft Store 安裝 Ubuntu

### 情況 2：OpenClaw 損壞

1. **重新安裝 OpenClaw**
   ```bash
   npm install -g openclaw
   ```

2. **Clone 最新備份**
   ```bash
   cd /home/feng/.openclaw/
   git clone git@github.com:149133f/piggy-backup.git workspace
   git clone git@github.com:149133f/jobs-backup.git workspace-jobs
   ```

3. **啟動 Gateway**
   ```bash
   openclaw gateway start
   ```

### 情況 3：忘記 SSH Key

1. **產生新的 SSH Key**
   ```bash
   ssh-keygen -t ed25519 -C "jobs@openclaw.ai" -f ~/.ssh/id_ed25519 -N ""
   ```

2. **複製公鑰並加到 GitHub**
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```

3. **驗證**
   ```bash
   ssh -T git@github.com
   ```

---

## 📞 GitHub 倉庫連結

| 倉庫 | URL |
|------|------|
| 小喬 | https://github.com/149133f/piggy-backup |
| Jobs | https://github.com/149133f/jobs-backup |
| Jarvis | https://github.com/149133f/jarvis-backup |

---

## ✅ 驗證清單

復原後檢查以下項目：

- [ ] `curl http://127.0.0.1:18789/health` 回應正常
- [ ] 小喬可以回應
- [ ] Jobs 可以回應
- [ ] Telegram 連線正常
- [ ] Git push/pull 正常
- [ ] 記憶檔案存在

---

如有問題，請聯繫師父！
