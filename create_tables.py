from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer, String, Numeric
)

engine = create_engine(
    "mysql+mysqlconnector://root:@127.0.0.1:3306/sandbox_db",
    future=True
)

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