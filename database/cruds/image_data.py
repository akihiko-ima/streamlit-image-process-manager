import pandas as pd
from sqlalchemy.orm import Session
from typing import Optional, List

from ..models import ImageData
from schemas.schemas import ImageDataCreate


def create_image_data(db: Session, image_data_create: ImageDataCreate) -> ImageData:
    """Create a new record in the ImageData table.

    Args:
        db (Session): The database session.
        image_data_create (ImageDataCreate): The data for creating a new ImageData record.

    Returns:
        ImageData: The created ImageData object.
    """
    current_time = pd.Timestamp.now(tz="UTC").tz_convert("Asia/Tokyo").floor("s")

    new_image_data = ImageData(
        file_name=image_data_create.file_name,
        file_path=image_data_create.file_path,
        file_extension=image_data_create.file_extension,
        file_size=image_data_create.file_size,
        description=image_data_create.description,
        uploaded_at=current_time,
        updated_at=current_time,
        is_processed=False,
    )
    db.add(new_image_data)
    db.commit()
    db.refresh(new_image_data)
    return new_image_data


def get_image_data_by_id(db: Session, image_data_id: int) -> Optional[ImageData]:
    """Retrieve a single ImageData record by its ID.

    Args:
        db (Session): The database session.
        image_data_id (int): The ID of the ImageData record to retrieve.

    Returns:
        ImageData: The retrieved ImageData object, or None if not found.
    """
    return db.query(ImageData).filter(ImageData.id == image_data_id).first()


def get_all_image_data(db: Session) -> List[dict]:
    """Retrieve all ImageData records as JSON.

    Args:
        db (Session): The database session.

    Returns:
        List[dict]: A list of ImageData objects in JSON format.
    """
    image_data = db.query(ImageData).all()
    return [data.to_dict() for data in image_data]


def update_image_data(
    db: Session,
    image_data_id: int,
    file_name: Optional[str] = None,
    file_path: Optional[str] = None,
    file_extension: Optional[str] = None,
    file_size: Optional[float] = None,
    description: Optional[str] = None,
    is_processed: Optional[bool] = None,
) -> Optional[ImageData]:
    """Update an ImageData record by its ID.

    Args:
        db (Session): The database session.
        image_data_id (int): The ID of the ImageData record to update.
        file_name (str, optional): The new file name. Defaults to None.
        file_path (str, optional): The new file path. Defaults to None.
        file_extension (str, optional): The new file extension. Defaults to None.
        file_size (float, optional): The new file size in bytes. Defaults to None.
        description (str, optional): The new description. Defaults to None.
        is_processed (bool, optional): The new processed status. Defaults to None.

    Returns:
        Optional[ImageData]: The updated ImageData object, or None if the record does not exist.
    """
    image_data = db.query(ImageData).filter(ImageData.id == image_data_id).first()
    if not image_data:
        return None

    current_time = pd.Timestamp.now(tz="UTC").tz_convert("Asia/Tokyo").floor("s")

    if file_name is not None:
        image_data.file_name = file_name
    if file_path is not None:
        image_data.file_path = file_path
    if file_extension is not None:
        image_data.file_extension = file_extension
    if file_size is not None:
        image_data.file_size = file_size
    if description is not None:
        image_data.description = description
    if is_processed is not None:
        image_data.is_processed = is_processed
    image_data.updated_at = current_time

    db.commit()
    db.refresh(image_data)
    return image_data


def delete_image_data(db: Session, image_data_id: int) -> bool:
    """Delete an ImageData record by its ID.

    Args:
        db (Session): The database session.
        image_data_id (int): The ID of the ImageData record to delete.

    Returns:
        bool: True if the record was deleted, False if not found.
    """
    image_data = db.query(ImageData).filter(ImageData.id == image_data_id).first()
    if not image_data:
        return False
    db.delete(image_data)
    db.commit()
    return True
