# Fathom OS - Solana Program Indexer

A high-performance, asynchronous blockchain indexer built for the Solana Devnet. It monitors a specific Program ID, extracts transaction metadata (Sender, Amount, Instructions), normalizes the data, and serves it via a REST API.

## Architecture & Tech Stack
* **Language:** Python 3.13
* **RPC Client:** `solana-py` / `solders` (Asynchronous)
* **Web Framework:** FastAPI / Uvicorn
* **Database:** PostgreSQL (via `asyncpg`)
* **ORM:** SQLAlchemy (AsyncSession)
* **Deployment:** Docker & Docker Compose

## Setup & Execution

**1. Environment Setup**
Create a `.env` file in the root directory based on the provided `.env.example` template:
```text
DATABASE_URL=postgresql+asyncpg://postgres:Nopassword123-!@db:5432/postgres
```

**2. Launch the System (Docker)**
This project is containerized for seamless execution. The following command will build the Python API environment and spin up the PostgreSQL database simultaneously.
```bash
docker-compose up --build -d
```

## API Documentation
Once the Docker containers are running, the background indexer will begin polling the Devnet. You can view the structured data via the REST API at `http://localhost:8001`.

* **System Status:** `GET /`
* **Fetch Transactions:** `GET /transactions?limit=10`
* **Interactive Swagger UI:** `GET /docs`

## Core Engineering Features
* **Idempotency:** Transactions are checked against the database via their unique base58 signatures prior to insertion, preventing data duplication during network polling.
* **Non-Blocking I/O:** Both the RPC network calls to the Solana cluster and the Database transactions utilize `asyncio` to prevent thread-locking.
* **Lamport Conversion:** Automatically calculates balance deltas from block metadata to determine the exact SOL amounts transferred.
* **Graceful Degradation:** Instruction decoding utilizes `try/except` fallbacks to handle raw binary data without crashing the indexer loop.