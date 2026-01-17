from sqlalchemy import (
    MetaData, Table, Column, Integer, String, Numeric)
from db import engine


metadata = MetaData()

items =  Table(
    "items",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("sku", String(50), nullable=False, unique=True),
    Column("name", String(255), nullable=False),
    Column("quantity", Integer, nullable=False, default=0),
    Column("price", Numeric(10, 2), nullable=False),
    
)

metadata.create_all(engine)

print("Table have been successfully created, you lucky dummy. hihihi.")