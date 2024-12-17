from sqlalchemy import Column, Integer, String, Text, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
import enum

Base = declarative_base()

class ContentTypeEnum(enum.Enum):
    url = "URL"
    base64 = "Base64"

class Document(Base):
    __tablename__ = 'database_document'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    file_extension = Column(String(10), nullable=False)
    type = Column(Enum(ContentTypeEnum), nullable=False, default=ContentTypeEnum.url)
    content = Column(Text, nullable=False)
    info = Column(JSON, nullable=True)

    def __repr__(self):
        return f"<Document(name='{self.name}', type='{self.type.name}')>"
