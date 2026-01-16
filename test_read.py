from sqlalchemy import create_engine, MetaData, Table, update, delete, select

engine = create_engine(
    "mysql+mysqlconnector://root:@127.0.0.1:3306/sandbox_db",
    future=True
)

metadata = MetaData()
items = Table("items", metadata, autoload_with=engine)

with engine.connect() as conn:
    result = conn.execute(select(items))
    for row in result:
        print(dict(row._mapping))