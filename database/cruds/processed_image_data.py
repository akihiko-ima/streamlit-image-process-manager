import pandas as pd
from sqlalchemy.orm import Session
from typing import Optional, List

from ..models import ProcessedImageData
from schemas.schemas import ProcessedImageDataCreate


def get_processed_image_data_by_id(
    db: Session, image_id: int
) -> Optional[ProcessedImageData]:
    """
    Retrieve a single ProcessedImageData record by its ID.

    Args:
        db (Session): The database session.
        image_id (int): The ID of the ProcessedImageData record to retrieve.

    Returns:
        Optional[ProcessedImageData]: The retrieved ProcessedImageData object, or None if not found.
    """
    return (
        db.query(ProcessedImageData).filter(ProcessedImageData.id == image_id).first()
    )


def get_all_processed_images(db: Session) -> List[dict]:
    """Retrieve all ProcessedImageData records as JSON.

    Args:
        db (Session): The database session.

    Returns:
        List[dict]: A list of ProcessedImageData objects in JSON format.
    """
    processed_images = db.query(ProcessedImageData).all()
    return [image.to_dict() for image in processed_images]


def create_processed_image_data(
    db: Session, image_data: ProcessedImageDataCreate
) -> ProcessedImageData:
    db_image_data = ProcessedImageData(**vars(image_data))
    db.add(db_image_data)
    db.commit()
    db.refresh(db_image_data)
    return db_image_data


def update_processed_image_data(
    db: Session, image_id: int, image_data: ProcessedImageDataCreate
) -> Optional[ProcessedImageData]:
    db_image_data = (
        db.query(ProcessedImageData).filter(ProcessedImageData.id == image_id).first()
    )
    if db_image_data:
        for key, value in vars(image_data).items():
            setattr(db_image_data, key, value)
        db.commit()
        db.refresh(db_image_data)
    return db_image_data


def delete_processed_image_data(
    db: Session, image_id: int
) -> Optional[ProcessedImageData]:
    db_image_data = (
        db.query(ProcessedImageData).filter(ProcessedImageData.id == image_id).first()
    )
    if db_image_data:
        db.delete(db_image_data)
        db.commit()
    return db_image_data
