from sqlalchemy import create_engine, MetaData, Table, update, delete, select

engine = create_engine(
    "mysql+mysqlconnector://root:@127.0.01:3306/sandbox_db",
    future=True
)

metadata = MetaData()
items = Table("items", metadata, autoload_with=engine)

with engine.connect() as conn:
    #UPDATE : change quantity of a specific SKU
    update_stmt = (
        update(items)
        .where(items.c.sku == "SKU-001")
        .values(quantity=25)
    )
    
    conn.execute(update_stmt)
    conn.commit()
    
    #DELETE: remove one SKU
    
    delete_stmt = delete(items).where(items.c.sku == "SKU-003")
    conn.execute(delete_stmt)
    conn.commit()
    
    # READ: show current state
    result = conn.execute(select(items))
    for row in result:
        print(dict(row._mapping))