import asyncio
import uvicorn
from api import app
from indexer import index_transactions


async def start_services():
    print("🚀 Fathom OS System Boot Sequence Initiated...")

    indexer_task = asyncio.create_task(index_transactions())

    config = uvicorn.Config(app, host="127.0.0.1", port=8001, log_level="info")
    server = uvicorn.Server(config)

    await server.serve()


if __name__ == "__main__":
    asyncio.run(start_services())