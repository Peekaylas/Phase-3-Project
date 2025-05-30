from sqlalchemy import Table, Column, Integer, ForeignKey
from .base import Base

category_transaction = Table(
    "category_transaction",
    Base.metadata,
    Column("transaction_id", Integer, ForeignKey("transactions.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("categories.id"), primary_key=True)
)