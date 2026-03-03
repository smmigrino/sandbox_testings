from sqlalchemy import MetaData, Table, select, update, insert
from db import engine

metadata = MetaData()
items = Table("items", metadata, autoload_with=engine)

#------ UPDATE QUANTITY FUNCTION WITH VALIDATION RULES ------
def update_quantity(sku: str, change: int):
    with engine.connect() as conn:
        
        if not sku or not sku.strip():
            print("Operation denied: SKU cannot be empty.")
            return
        
        if not isinstance(change, int):
            print("Operation denied: change must be an integer.")
            return
        
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

#------ CREATE / ADD ITEM FUNCTION WITH VALIDATION RULES ------
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
    
    if not isinstance(price, (int, float)):
        print("Operation denied: PRICE must be a number.")
        return
    
    if price < 0:
        print("Operation denied: PRICE must not be a negative value.")
        return
    
    # ---- Database Operation ----
    
    with engine.connect() as conn:
        #Check if SKU exist
        existing_sku = conn.execute(
            select(items.c.id).where(items.c.sku == sku)
        ).fetchone()
        
        if existing_sku:
            print(f"Operation Denied: SKU {sku} already exist")
            return
            
        existing_name = conn.execute(
            select(items.c.id).where(items.c.name == name)
        ).fetchone()
        
        if existing_name:
            print(f"Operation Denied: NAME {name} already exist")
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
#create_item("Tex-A0001","Auburn silk", 47, 9)
#create_item("Tex-A0002","Torquuoise silk", 9, 7)
#create_item("SKU-010", "New Item", 5, 50.00)     # VALID
#create_item("", "No SKU", 5, 10.00)              # INVALID
#create_item("SKU-010", "Duplicate", 3, 20.00)    # DUPLICATE
#create_item("SKU-011", "Bad Price", 5, -10)      # INVALID

#--------------------------------------------

#------ DELETE ITEM FUNCTION WITH VALIDATION RULES ------
def delete_item(sku: str):
    # ---- Basic Validation ----
    if not sku or not sku.strip():
        print("Operation denied: SKU cannot be empty.")
        return
    
    # ---- Database Operation ----
    with engine.connect() as conn:
        result = conn.execute(
            select(items.c.id).where(items.c.sku == sku)
        ).fetchone()
        
        if result is None:
            print(f"SKU {sku} not found.")
            return
        
        conn.execute(
            items.delete().where(items.c.sku == sku)
        )
        conn.commit()
        print(f"SKU {sku} successfully deleted.")   
        
#---test cases----
#delete_item("SKU-010")   #VALID
#delete_item("")          #INVALID
#delete_item("SKU-999")   #MISSING SKU

#--------------------------------------------
#------ PRINT ITEM FUNCTION WITH VALIDATION RULES ------
    #user input can be either SKU or NAME, but not both empty. If both provided,
    #it will search for items matching either criteria (OR condition).

def print_item(sku: str = None, name: str = None):

    if (not sku or not sku.strip()) and (not name or not name.strip()):
        print("Operation denied: provide SKU or NAME.")
        return

    with engine.connect() as conn:

        query = select(items)

        if sku and sku.strip():
            query = query.where(items.c.sku == sku)

        if name and name.strip():
            query = query.where(items.c.name == name)

        result = conn.execute(query).fetchall()

        if not result:
            print("No matching item found.")
            return

        for row in result:
            print(
                f"ID: {row.id}, "
                f"SKU: {row.sku}, "
                f"NAME: {row.name}, "
                f"QUANTITY: {row.quantity}, "
                f"PRICE: {row.price}"
            )