from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Float
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class VaultTransaction(Base):
    __tablename__ = 'vault_transactions'

    id = Column(Integer, primary_key=True)
    signature = Column(String, unique=True, nullable=False)
    slot = Column(BigInteger, nullable=False)
    block_time = Column(DateTime, default=datetime.utcnow)
    instruction = Column(String)
    sender = Column(String)
    amount = Column(Float)