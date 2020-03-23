from sqlalchemy.orm import sessionmaker
from orm_db.models import Points
from base import engine


Session = sessionmaker(bind=engine)
session = Session()

for instance in session.query(Points):
    print(instance.id)

session.close()