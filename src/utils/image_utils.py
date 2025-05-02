import os
from sqlalchemy.orm import Session
from typing import List
from PIL import Image

from database.database import get_db_session
from database.cruds.image_data import (
    create_image_data,
    get_image_data_by_id,
    delete_image_data,
)
from schemas.schemas import ImageDataCreate


def save_image(image: Image.Image, file_name: str, save_path: str, db: Session) -> None:
    """
    画像を保存し、データベースに登録し、通知を送信する。

    Args:
        image (Image.Image): 保存するPIL画像オブジェクト。
        file_name (str): 保存先のファイル名。
        save_path (str): 保存先のディレクトリパス。
        db (DatabaseSession): データベースセッションオブジェクト。
    """
    file_path = os.path.join(save_path, file_name)
    image.save(file_path)

    # データベースに保存
    new_image_data = ImageDataCreate(
        file_name=file_name,
        file_path=file_path,
        file_extension=file_name.split(".")[-1],
        file_size=os.path.getsize(file_path),
        description="",
    )
    with get_db_session() as db:
        create_image_data(db=db, image_data_create=new_image_data)


def delete_image_db_and_folder(db: Session, image_id_list: List[int]) -> None:
    for image_id in image_id_list:
        image_data = get_image_data_by_id(db, image_id)

        if image_data and os.path.exists(image_data.file_path):
            os.remove(image_data.file_path)

        with get_db_session() as db:
            delete_image_data(db, image_id)
