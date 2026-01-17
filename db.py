from sqlalchemy import create_engine

engine = create_engine(
    "mysql+mysqlconnector://root:@127.0.0.1:3306/sandbox_db", future=True
)