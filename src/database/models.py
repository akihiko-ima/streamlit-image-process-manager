import pandas as pd
from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Boolean

from .database import Base


class ImageData(Base):
    __tablename__ = "image_data"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    file_path = Column(String, index=True)
    file_extension = Column(String, index=True)
    file_size = Column(Float)
    description = Column(String)
    is_processed = Column(Boolean, default=False)
    uploaded_at = Column(
        DateTime, default=pd.Timestamp.now(tz="UTC").tz_convert("Asia/Tokyo").floor("s")
    )
    updated_at = Column(
        DateTime, default=pd.Timestamp.now(tz="UTC").tz_convert("Asia/Tokyo").floor("s")
    )

    def to_dict(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "file_extension": self.file_extension,
            "file_size": self.file_size,
            "uploaded_at": self.uploaded_at,
            "updated_at": self.updated_at,
            "is_processed": self.is_processed,
            "description": self.description,
        }


class ProcessedImageData(Base):
    __tablename__ = "processed_image_data"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)
    file_path = Column(String, index=True)
    processed_at = Column(
        DateTime, default=pd.Timestamp.now(tz="UTC").tz_convert("Asia/Tokyo").floor("s")
    )

    def to_dict(self):
        return {
            "id": self.id,
            "file_name": self.file_name,
            "file_path": self.file_path,
            "processed_at": self.processed_at,
        }


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, index=True)
    created_at = Column(
        DateTime, default=pd.Timestamp.now(tz="UTC").tz_convert("Asia/Tokyo").floor("s")
    )
