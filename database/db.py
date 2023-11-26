from sqlalchemy import create_engine, text
from model import Base, Users, FinanceInfo
from sqlalchemy.orm import Session
from instance.config import SQLALCHEMY_DATABASE_URI

engine = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)

with engine.connect() as connections:
    result = connections.execute(text("select 'hello world'"))
    print(result.all())

print("CreatingTables")
Base.metadata.create_all(bind=engine)
