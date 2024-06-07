from sqlalchemy import create_engine, Column, Integer, String, Numeric
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import update
from Postgres.config import user, password, database_name

# создание объекта Engine для PostgreSQL базы данных
engine = create_engine(f'postgresql+psycopg2://{user}:{password}@localhost:5432/{database_name}', echo=True)

# определение базового класса моделей
Base = declarative_base()

# определение модели данных для таблицы "currencies"
class Currency(Base):
    __tablename__ = 'currencies'

    id = Column(Integer, primary_key=True)
    currency_name = Column(String)
    rate = Column(Numeric)

# определение модели данных для таблицы admins
class Admin(Base):
    __tablename__ = 'admins'

    id = Column(Integer, primary_key=True)
    chat_id = Column(String)

# создание таблиц в базе данных
Base.metadata.create_all(engine)

# создание объекта сессии для взаимодействия с базой данных
Session = sessionmaker(bind=engine)
session = Session()

# фиксация изменений в базе данных
session.commit()

# закрытие сессии
session.close()


