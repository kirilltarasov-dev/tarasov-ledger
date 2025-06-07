# 🧾 tarasovLedger

> A full-stack-ready microservice for OCR-based financial document ingestion and structured transaction parsing, built with FastAPI + OpenAI + PostgreSQL.

---

## 🚀 Features

- Upload receipts, invoices, or bank statements as images
- OCR-based text extraction using Tesseract
- LLM-powered parsing of raw text into structured transaction fields
- Regex-based fallback parser (if LLM fails)
- PostgreSQL backend for storage
- Dockerized & production-ready

---

## 📦 Tech Stack

- **Python 3.11**
- **FastAPI** + Pydantic
- **PostgreSQL** with SQLAlchemy async ORM
- **Docker** + Docker Compose
- **OpenAI GPT-3.5** (optional, configurable)
- **Tesseract OCR** (via `pytesseract`)

---

## 📸 Example Workflow

1. Upload image via `/upload`
2. App extracts raw text via OCR
3. Text is parsed using GPT (or fallback logic)
4. Transaction is saved in DB:
   - `vendor`, `amount`, `date`, `category`, etc.

---

## 🛠️ Setup

### 1. Clone the repo

```bash
git clone https://github.com/your-username/tarasov-ledger.git
cd tarasov-ledger
```

### 2. Create `.env`

```bash
cp .env.sample .env
```

Edit `.env` and fill in your `DATABASE_URL` and `OPENAI_API_KEY`.

### 3. Run with Docker Compose

```bash
docker-compose up --build
```

---

## ✅ Manual Testing

```bash
curl -X POST http://localhost:8000/upload \
  -F "file=@/path/to/receipt.jpg"
```

You’ll receive structured transaction info in response.

---

## 🧠 Example Use Cases

- Personal finance automation
- Expense tracking
- Bookkeeping pre-processing
- Building financial datasets from raw scans

---

## 📈 Planned Features

- Transaction search & filters
- Insights dashboard (30-day spend, category breakdown)
- CSV export
- Budget tagging
- LLM-powered categorization tuning
