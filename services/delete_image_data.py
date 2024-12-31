import os
from sqlalchemy.orm import Session
from typing import List

from database.cruds.image_data import get_image_data_by_id, delete_image_data


def delete_image_db_and_folder(db: Session, image_id_list: List[int]) -> None:
    for image_id in image_id_list:
        image_data = get_image_data_by_id(db, image_id)

        # フォルダから削除
        if image_data and os.path.exists(image_data.file_path):
            os.remove(image_data.file_path)

        # データベースから削除
        delete_image_data(db, image_id)
