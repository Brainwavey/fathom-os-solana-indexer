import uvicorn
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import async_session
from models import VaultTransaction

app = FastAPI(title="Fathom OS Indexer API")


# This creates a safe database connection for every web request
async def get_db():
    async with async_session() as session:
        yield session


@app.get("/")
async def root():
    return {"status": "🟢 Online", "system": "Fathom OS Indexer is running"}


@app.get("/transactions")
async def fetch_transactions(limit: int = 10, db: AsyncSession = Depends(get_db)):
    # Ask the database for the most recent transactions
    stmt = select(VaultTransaction).order_by(VaultTransaction.block_time.desc()).limit(limit)
    result = await db.execute(stmt)
    transactions = result.scalars().all()

    return {
        "network": "Solana Devnet",
        "count": len(transactions),
        "data": transactions
    }


if __name__ == "__main__":
    # This starts the web server on port 8000
    uvicorn.run("api:app", host="127.0.0.1", port=8000, reload=True)