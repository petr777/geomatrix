from sqlalchemy.orm import sessionmaker
from orm_db.models import Points
from base import engine


Session = sessionmaker(bind=engine)
session = Session()

for instance in session.query(Points):
    print(instance.id)

session.close()
"""
file = 'yves_pd_data_new.xlsx'
df = pd.read_excel(file, index_col=0)

for index, row in df.iterrows():
    vasiaUser = Points(
        country=None,
        region=row['region'],
        city=row['city'],
        post_code=row['post_code'],
        address=row['address'],
        name_TC=row['name_TC'],
        working_time=row['working_time'],
        x=row['x'],
        y=row['y'],
        brand_name=row['brand_name'],
        holding_name=row['holding_name'],
        website=row['website'],
        date_review=row['date_review']
    )
    session.add(vasiaUser)

session.commit()
"""