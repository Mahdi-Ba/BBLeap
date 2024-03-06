from sqlalchemy import Column, DateTime, Integer, String, func, Text, Date, ForeignKey, JSON, Enum as SQLEnum
from core.base_model import Base
from sqlalchemy.dialects.postgresql import UUID
import uuid
from sqlalchemy.orm import relationship
from geoalchemy2 import Geometry


class Area(Base):
    id = Column(Integer, primary_key=True)
    uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    name = Column(String)
    geometry = Column(Geometry('POLYGON'))
    created_at = Column(DateTime, default=func.now(), nullable=False)


    def __repr__(self):
        return f"<Field(id={self.id}, name={self.name}, geometry={self.geometry})>"
