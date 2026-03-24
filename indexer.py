import asyncio
import os
from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select
from dotenv import load_dotenv

# Import our database structure
from database import engine
from models import VaultTransaction

load_dotenv()

PROGRAM_ID = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")
RPC_URL = "https://api.devnet.solana.com"

# Setup the Database Session
async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def index_transactions():
    async with AsyncClient(RPC_URL) as client:
        print(f"📡 Indexer Started. Monitoring Program: {PROGRAM_ID}")

        while True:
            try:
                # 1. Fetch the latest signatures
                response = await client.get_signatures_for_address(PROGRAM_ID, limit=10)
                signatures = response.value

                async with async_session() as session:
                    for sig_info in signatures:
                        signature_str = str(sig_info.signature)

                        # 2. Check if we already indexed this transaction
                        stmt = select(VaultTransaction).where(VaultTransaction.signature == signature_str)
                        result = await session.execute(stmt)
                        if result.scalar():
                            continue

                        print(f"🔍 Decoding New Transaction: {signature_str}")

                        # --- THE DECODER (NEW LOGIC) ---
                        sender_address = "Unknown"
                        instruction_data = "Unknown"
                        amount_moved = 0.0

                        try:
                            # Fetch the full details of this specific transaction
                            tx_response = await client.get_transaction(
                                sig_info.signature,
                                max_supported_transaction_version=0
                            )

                            if tx_response.value and tx_response.value.transaction:
                                tx = tx_response.value.transaction.transaction
                                meta = tx_response.value.transaction.meta

                                # A. Get the Sender (The Fee Payer is always index 0)
                                sender_address = str(tx.message.account_keys[0])

                                # B. Get the Amount (Calculate the change in SOL balance)
                                if meta:
                                    pre_balance = meta.pre_balances[0]
                                    post_balance = meta.post_balances[0]
                                    # Solana uses Lamports (1 SOL = 1,000,000,000 Lamports)
                                    amount_moved = abs(pre_balance - post_balance) / 10 ** 9

                                # C. Get the Instruction (Decode the Memo text)
                                if hasattr(tx.message, 'instructions') and len(tx.message.instructions) > 0:
                                    raw_data = tx.message.instructions[0].data
                                    try:
                                        # The Memo program stores data as UTF-8 text
                                        instruction_data = raw_data.decode('utf-8')
                                    except:
                                        instruction_data = "Encoded Binary Data"

                        except Exception as decode_error:
                            print(f"⚠️ Could not decode details: {decode_error}")
                        # -------------------------------

                        # 3. Create a new record with the REAL data
                        new_tx = VaultTransaction(
                            signature=signature_str,
                            slot=sig_info.slot,
                            instruction=instruction_data,
                            sender=sender_address,
                            amount=amount_moved
                        )

                        session.add(new_tx)

                    await session.commit()

                # Wait before checking again
                await asyncio.sleep(10)

            except Exception as e:
                print(f"⚠️ Error in Indexer Loop: {e}")
                await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(index_transactions())