from sqlalchemy import create_engine, MetaData, Table, insert, select

engine = create_engine(
    "mysql+mysqlconnector://root:@127.0.0.1:3306/sandbox_db",
    future=True
)

metadata = MetaData()
items = Table("items", metadata, autoload_with=engine)

with engine.connect() as conn:
    # INSERT (Sample item)
    stmt = insert(items).values(
        sku="SKU-001",
        name="Sample Item 1",
        quantity=10,
        price=99.99
    )
    
    conn.execute(stmt)
    conn.commit()
    
    # SELECT (read all items)
    result = conn.execute(select(items))
    for row in result:
        print(dict(row))