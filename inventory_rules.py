from sqlalchemy import create_engine, MetaData, Table, select, update
from db import engine

metadata = MetaData()
items = Table("items", metadata, autoload_with=engine)

def update_quantity(sku: str, change: int):
    with engine.connect() as conn:
        # READ current quantity
        result = conn.execute(
            select(items.c.quantity).where(items.c.sku == sku)
        ).fetchone()
        
        if result is None:
            print(f"SKU {sku} not found.")
            return
        
        current_qty = result.quantity
        new_qty = current_qty + change
        
        if new_qty < 0 :
            print("Operation denied: stock cannot be a negative value.")
            return
        
        conn.execute(
            update(items)
            .where(items.c.sku == sku)
            .values(quantity=new_qty)
        )
        conn.commit()
        print(f"SKU {sku} updated: {current_qty} -> {new_qty}")
        
# ------ test cases ------

update_quantity("SKU-001", -5)    #VALID
update_quantity("SKU-001", -100)  #INVALID
update_quantity("SKU-0999", -5)  #MISSING SKU

        

         