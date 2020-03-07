from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Numeric

meta = MetaData()
engine = create_engine('sqlite:///geo_data.db', echo=True)

retail_points = Table(
    'retail_points', meta,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False),
    Column('brand_name', String, nullable=False),
    Column('x', Numeric(12, 2)),
    Column('y', Numeric(12, 2)),
    Column('address', String, nullable=True),
    Column('date_review', DateTime)
)

meta.create_all(engine)