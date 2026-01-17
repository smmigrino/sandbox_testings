from sqlalchemy import create_engine, MetaData, Table, insert, select
from db import engine

metadata = MetaData()
items = Table("items", metadata, autoload_with=engine)

with engine.connect() as conn:
    # INSERT (Sample item)
    stmt = insert(items).values(
        sku="SKU-003",
        name="Sample Item 1",
        quantity=10,
        price=99.99
    )
    
    conn.execute(stmt)
    conn.commit()
    
    # SELECT (read all items)
    result = conn.execute(select(items))
    for row in result:
        print(dict(row._mapping))