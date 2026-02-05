# Broker-Aware Algo Trading System (Python)

Production-oriented algorithmic trading system built in Python with
broker-aware execution, risk controls, and separate PAPER / LIVE engines.

This project demonstrates how real-world algo trading systems are designed,
debugged, and operated with Indian broker APIs (Angel One).

---

## 🚀 Key Features

- Broker-aware order execution (Angel One SmartAPI)
- Separate LIVE and PAPER trading engines
- Pre-trade margin validation using RMS limits
- Stop Loss, Target & Trailing SL logic
- Partial fill simulation in PAPER mode
- Real-time LTP monitoring
- Excel-based trade & order audit logs
- Telegram alerts for entry, exit, and errors
- Clean modular architecture (OMS-style)

---

## 🧠 Why This Project?

Most beginner algo projects only place orders.

This system focuses on **production realities**:
- Broker rejections
- Margin shortfall handling
- API rate limits
- Paper vs live divergence
- Risk-first execution
- Trade observability (logs + alerts)

The goal is not backtesting only — but **execution infrastructure**.

---

## 🏗️ System Architecture

main.py
│
├── broker.py # Angel One login, search, RMS, order APIs
├── engine_live.py # LIVE trading engine (real orders)
├── engine_paper.py # PAPER trading engine (simulated fills)
├── orders.py # Order placement & status handling
├── risk.py # SL / Target / Trailing SL logic
├── excel_logger.py # Trade lifecycle logging (entry → exit)
├── telegram.py # Telegram alert system
├── token_master.py # Symbol discovery & token resolution
├── config.example.py # Safe config template (no secrets)
└── .gitignore # Protect secrets, logs, venv


---

## 🔄 Trading Flow

### 1️⃣ Symbol Discovery
- User enters stock name (e.g. SBIN, INFY)
- Broker search API resolves exact tradingsymbol & token

### 2️⃣ Pre-Trade Checks
- Fetch LTP
- Validate quantity
- LIVE mode → RMS margin check
- Block order if insufficient funds

### 3️⃣ Entry Execution
- PAPER: simulated entry (supports partial fills)
- LIVE: real order placement via broker API

### 4️⃣ Risk Attachment
- Initial Stop Loss
- Target
- Trailing SL logic

### 5️⃣ Monitoring
- Continuous LTP polling
- Terminal display updates in-place
- SL / Target / Manual exit handling

### 6️⃣ Exit & Logging
- Exit reason recorded
- Excel trade log updated
- Telegram alert sent

---

## ⚠️ PAPER vs LIVE (Important)

| Aspect | PAPER | LIVE |
|------|------|------|
Execution | Simulated | Real broker orders |
Partial fills | ✅ Yes | Broker dependent |
Margin check | ❌ Not required | ✅ Mandatory |
Risk logic | Same | Same |
Alerts | ✅ | ✅ |

This separation avoids accidental live trades and enables safe testing.

---

## 📊 Sample Terminal Output

TCS-EQ | LTP:3186.90 | SL:3176.90 | TARGET:3206.90 | P&L:0.00


(Price updates dynamically at the same terminal line)

---

## 🔔 Alerts

Telegram alerts are sent for:
- Entry placed
- Order rejected
- Exit (SL / Target / Manual)
- Paper trade lifecycle

---

## 📁 Configuration & Security

- **DO NOT** commit real API keys
- Copy `config.example.py` → `config.py`
- Add secrets locally only
- `.gitignore` ensures sensitive files are never pushed

---

## 🧩 Open Roadmap (GitHub Issues)

- WebSocket-based live market data
- Persist orders & positions in database
- Dockerized deployment for cloud
- Multi-strategy execution framework

---

## 👤 Author

**Shivakumar**  
Quant / Algo Trading Systems Developer  
Python | Broker APIs | OMS | Risk & Execution  
LinkedIn: https://www.linkedin.com/in/shivakumar-quant

---

## ⚖️ Disclaimer

This project is for educational and infrastructure demonstration purposes.
Live trading involves financial risk.
