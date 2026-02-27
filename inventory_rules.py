from sqlalchemy import MetaData, Table, select, update, insert
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

#update_quantity("SKU-001", -5)    #VALID
#update_quantity("SKU-001", -100)  #INVALID
#update_quantity("SKU-0999", -5)  #MISSING SKU

#--------------------------------------------


def create_item(sku: str, name: str, quantity: int, price: float):
    # ---- Basic Validation ----
    if not sku or not sku.strip():
        print("Operation denied: SKU cannot be empty.")
        return
    
    if not name or not name.strip():
        print("Operation denied: NAME cannot be empty.")
        return
    
    if not isinstance(quantity, int):
        print("Operation denied: QUANTITY must be an integer.")
        return
    
    if quantity < 0:
        print("Operation denied: QUANTITY must not be a negative value.")
        return
        
    if price < 0:
        print("Operation denied: PRICE must not be a negative value.")
        return
    
    # ---- Database Operation ----
    
    with engine.connect() as conn:
        #Check if SKU exist
        existing = conn.execute(
            select(items.c.id).where(items.c.sku == sku)
        ).fetchone()
        
        if existing:
            print(f"Operation Denied: SKU {sku} already exist")
            return
            
        conn.execute(
            insert(items).values(
                sku=sku,
                name=name,
                price=price,
                quantity=quantity
            )
        )
        conn.commit()
        
        print(f"Item {sku} successfully created.")
        
#---test cases----
create_item("Tex-A0001","Auburn silk", 4, 9)
create_item("Tex-A0002","Torquuoise silk", 8, 7)