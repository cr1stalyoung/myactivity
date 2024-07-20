from sqlalchemy import Column, Integer, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class GuildModel(Base):
    __tablename__ = 'guild'

    id = Column(Integer, nullable=False, primary_key=True)
    guild_id = Column(BigInteger, nullable=False)
    first_case = Column(Integer, nullable=False)
    second_case = Column(Integer, nullable=False)
    third_case = Column(Integer, nullable=False)
    total_case = Column(Integer, nullable=False)
    fourth_case = Column(Integer, nullable=False)
    fifth_case = Column(Integer, nullable=False)
    sixth_case = Column(Integer, nullable=False)
