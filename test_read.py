from sqlalchemy import MetaData, Table, select
from db import engine

metadata = MetaData()
items = Table("items", metadata, autoload_with=engine)

with engine.connect() as conn:
    result = conn.execute(select(items))
    for row in result:
        print(dict(row._mapping))