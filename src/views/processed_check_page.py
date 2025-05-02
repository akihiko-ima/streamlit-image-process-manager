import streamlit as st
import cv2
import pandas as pd
from PIL import Image
from sqlalchemy.orm import Session

from services.initialize_setting import initialize_setting
from database.database import get_db_session
from database.cruds.processed_image_data import (
    get_all_processed_images,
    get_processed_image_data_by_id,
)
from utils.format_datetime_column import format_datetime_column
from utils.aggrid_dataframe import configure_aggrid


def show():
    # --------------- initialized ---------------
    initialize_setting()

    st.title(":material/folder_managed: 画像処理結果確認")

    with get_db_session() as db:
        processed_image_data_list = get_all_processed_images(db=db)

    # データフレームの作成
    if len(processed_image_data_list) > 0:
        df_processed_img = pd.DataFrame(processed_image_data_list)
        df_processed_img = format_datetime_column(df_processed_img, "processed_at")

        # ユーザーが選択したデータ情報を取得
        selected_df = configure_aggrid(df_processed_img)
        if not selected_df.empty:
            selected_processed_id_list = selected_df["id"].tolist()
            st.session_state["selected_processed_id_list"] = selected_processed_id_list

    # checkboxを選択していない場合は空リストをセット
    if "selected_processed_id_list" not in st.session_state:
        st.session_state["selected_processed_id_list"] = []

    if st.button(
        label="画像処理結果確認",
        key="view_processed_image_data",
        type="primary",
        icon=":material/search:",
    ):
        if len(st.session_state["selected_processed_id_list"]) == 0:
            st.toast("画像を選択してください", icon="🚨")
        else:
            for image_id in st.session_state["selected_processed_id_list"]:
                with get_db_session() as db:
                    image_data = get_processed_image_data_by_id(
                        db=db, image_id=image_id
                    )

                if image_data is not None:
                    image = cv2.imread(image_data.file_path)
                    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                    st.image(
                        image_rgb,
                        caption=str(image_data.file_name),
                        use_container_width=True,
                    )
                else:
                    st.toast("画像データが見つかりませんでした", icon="🚨")
