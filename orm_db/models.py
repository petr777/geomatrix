from sqlalchemy import Table, Column, Integer, String, MetaData, DateTime, Numeric
from base import Base



class Points(Base):
    __tablename__ = 'points'
    id = Column(Integer, primary_key=True)
    country = Column(String)
    region = Column(String)
    city = Column(String)
    post_code = Column(String)
    address = Column(String)
    name_TC = Column(String)
    working_time = Column(String)
    x = Column(Numeric(12, 2))
    y = Column(Numeric(12, 2))
    brand_name = Column(String)
    holding_name = Column(String)
    website = Column(String)
    date_review = Column(DateTime)

    def __init__(self, country, region, city, post_code,
                 address, name_TC, working_time, x, y,
                 brand_name, holding_name, website, date_review):

        self.country = country
        self.region = region
        self.city = city
        self.post_code = post_code
        self.address = address
        self.name_TC = name_TC
        self.working_time = working_time
        self.x = x
        self.y = y
        self.brand_name = brand_name
        self.holding_name = holding_name
        self.website = website
        self.date_review = date_review

    def __repr__(self):
        return "<User('%s','%s', '%s')>" % (self.address, self.x, self.y)


# Создание таблицы
#Base.metadata.create_all(engine)