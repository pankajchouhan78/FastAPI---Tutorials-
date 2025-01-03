# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import Session

# # Eastlish a connection to the database

# db_url="postgres://postgres:admin@localhost:5432/crudinfastapi"
# engine = create_engine(db_url)
# session = Session(engine)


from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker


url = URL.create(
    drivername="postgresql",
    username="postgres",
    password="admin",
    host="localhost",
    database="crudinfastapi",
    port=5432
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
