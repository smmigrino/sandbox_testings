from sqlalchemy import create_engine, text

engine = create_engine(
    "mysql+mysqlconnector://root@127.0.0.1:3306/sandbox_db",
    future=True
)

with engine.connect() as conn:
    version = conn.execute(text("SELECT VERSION()")).scalar()
    print("Connection to MySQL:", version)
    
    