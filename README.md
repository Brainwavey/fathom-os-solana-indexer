# Fathom OS - Solana Program Indexer 🚀

A high-performance, asynchronous blockchain indexer built for the Solana Devnet. This system monitors a specific Program ID, extracts transaction metadata (Sender, Amount, Instructions), normalizes the data into a relational database, and serves it via a REST API.

## 🛠 Tech Stack
* **Language:** Python 3.13
* **Blockchain:** `solana-py` / `solders` (Asynchronous RPC)
* **API:** FastAPI / Uvicorn
* **Database:** PostgreSQL (via `asyncpg`)
* **ORM:** SQLAlchemy (AsyncSession)
* **DevOps:** Docker & Docker Compose

## 🏗 Architecture
The system uses an **asynchronous orchestrator** to run the background indexer and the FastAPI server concurrently on a single thread, ensuring high efficiency on limited hardware.

### Key Features:
* **Idempotency:** Unique transaction signatures prevent data duplication.
* **Non-Blocking I/O:** Uses `asyncio` for both network and database operations.
* **Precision Math:** Converts raw Lamports to SOL with native balance delta calculations.
* **Error Handling:** Gracefully handles encoded binary data in instructions.

## 🚀 Getting Started

1. **Clone the repo**
2. **Setup Environment:** Create a `.env` file from the `.env.example` template.
3. **Run with Docker:**
   ```bash
   docker-compose up --build -d
   📡 API Endpoints
System Health: GET /

Indexed Data: GET /transactions

Swagger Documentation: GET /docs
