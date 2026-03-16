from sqlalchemy import Column, Integer, String, DateTime, Text
from app.database import Base

class BitMatrix(Base):
    __tablename__ = "bit_matrices"
    
    id = Column(Integer, primary_key=True, index=True)
    dimension = Column(Integer)
    branch_number = Column(Integer)
    depth = Column(Integer, nullable=True)
    xor_count = Column(Integer)
    matrix = Column(Text)
    add_time = Column(DateTime)

class SBox(Base):
    __tablename__ = "sboxes"
    
    id = Column(Integer, primary_key=True, index=True)
    sbox = Column(Text)
    add_time = Column(DateTime)

    