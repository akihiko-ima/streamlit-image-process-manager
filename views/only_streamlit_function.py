import os
import base64
import cv2
import time
import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from PIL import Image

from services.initialize_setting import initialize_setting
from services.dummy_heavy_image_processing import dummy_heavy_image_processing
from database.database import get_db_session
from database.cruds.image_data import (
    create_image_data,
    get_all_image_data,
    update_image_data,
    get_image_data_by_id,
)
from database.cruds.processed_image_data import create_processed_image_data
from schemas.schemas import ImageDataCreate, ProcessedImageDataCreate
from utils.format_datetime_column import format_datetime_column
from utils.send_line_message import send_line_message
from utils.encode_image import encode_image
from utils.image_utils import save_image, delete_image_db_and_folder


def show():
    # --------------- initialized ---------------
    initialize_setting()

    # Define a function to display a message dialog
    @st.dialog("この機能は今後開発予定です。")
    def message_dialog(message):
        st.write(f"{message}")

    st.title(":material/folder_managed: 画像処理マネージャー")

    if st.sidebar.button(
        label="リセット",
        key="reset",
        type="primary",
        icon=":material/refresh:",
    ):
        st.rerun()

    # --------------- 画像アップロードセクション ---------------
    st.subheader(":material/cloud_upload: 画像アップロード", divider="gray")

    take_photo = st.toggle("📸 Take a photo?")

    if take_photo:
        picture = st.camera_input("Take a picture", label_visibility="hidden")

        if picture:
            st.image(picture)

            # 保存ボタンを表示
            if st.button(
                label="撮影した画像を保存する",
                key="save_camera_image",
                type="primary",
                icon=":material/cloud_upload:",
            ):
                camera_file_name = f"camera_image_{int(time.time())}.png"
                image: Image.Image = Image.open(picture)
                with get_db_session() as db:
                    save_image(
                        image, camera_file_name, st.session_state.data_raw_path, db
                    )

                # 保存をLINEに通知
                message_text = f"画像が保存されました: {camera_file_name}\nURLはこちらです。=> https://imaima-image-process-manager.streamlit.app/"
                send_line_message(
                    USER_ID=st.secrets["LINE_USER_ID"],
                    CHANNEL_ACCESS_TOKEN=st.secrets["LINE_CHANNEL_ACCESS_TOKEN"],
                    messageText=message_text,
                    log_file_path="./log/line_message.log",
                )
                st.toast("画像が保存されました", icon="🎉")
                time.sleep(1)
                st.rerun()

    else:
        uploaded_files = st.file_uploader(
            label="画像をアップロードしてください",
            type=["png", "jpg", "jpeg"],
            accept_multiple_files=True,
            label_visibility="hidden",
        )

        if uploaded_files:
            if st.button(
                label="画像を保存する",
                key="save_image_data",
                type="primary",
                icon=":material/cloud_upload:",
            ):
                for uploaded_file in uploaded_files:
                    image = Image.open(uploaded_file)
                    with get_db_session() as db:
                        save_image(
                            image,
                            uploaded_file.name,
                            st.session_state.data_raw_path,
                            db,
                        )

                # 保存をLINEに通知
                message_text = f"画像が保存されました: {uploaded_file.name}\nURLはこちらです。=> https://imaima-image-process-manager.streamlit.app/"
                send_line_message(
                    USER_ID=st.secrets["LINE_USER_ID"],
                    CHANNEL_ACCESS_TOKEN=st.secrets["LINE_CHANNEL_ACCESS_TOKEN"],
                    messageText=message_text,
                    log_file_path="./log/line_message.log",
                )
                st.toast("画像が保存されました", icon="🎉")
                time.sleep(1)
                st.rerun()

    # --------------- データベーステーブルセクション ---------------
    st.subheader(":material/database: Image database", divider="gray")

    with get_db_session() as db:
        image_data_list = get_all_image_data(db=db)

    # データフレームの作成
    if len(image_data_list) > 0:
        df_raw_img = pd.DataFrame(image_data_list)

        df_raw_img["image"] = df_raw_img["file_path"].apply(encode_image)
        df_raw_img["is_processed"] = df_raw_img["is_processed"].apply(
            lambda x: "済" if x else "未"
        )
        df_raw_img = format_datetime_column(df_raw_img, "uploaded_at")
        df_raw_img = format_datetime_column(df_raw_img, "updated_at")

        df_raw_img["Select"] = [False] * len(df_raw_img)

        column_config = {
            "id": st.column_config.NumberColumn("ID"),
            "file_name": st.column_config.TextColumn("ファイル名"),
            "file_path": st.column_config.TextColumn("ファイルパス"),
            "file_size": st.column_config.NumberColumn(
                "ファイルサイズ (KB)", format="%d"
            ),
            "is_processed": st.column_config.TextColumn("処理状態"),
            "image": st.column_config.ImageColumn("画像"),
        }

        columns_order = [
            "Select",
            "id",
            "image",
            "file_name",
            "file_path",
            "file_extension",
            "file_size",
            "uploaded_at",
            "updated_at",
            "is_processed",
            "description",
        ]

        # DataFrame の列を並び替え
        df_raw_img = df_raw_img[columns_order]
        edited_df = st.data_editor(
            df_raw_img, column_config=column_config, hide_index=True
        )

        # 選択された行のチェック
        if edited_df is not None and "Select" in edited_df:
            selected_rows = edited_df[edited_df["Select"] == True]

            if not selected_rows.empty:
                selected_id_list = selected_rows["id"].tolist()
                st.session_state.selected_id_list = selected_id_list
            else:
                st.session_state.selected_id_list = []
    else:
        st.write("No image data available.")

    # --------------- ボタンセクション ---------------
    left_button, middle_button, right_button = st.columns(3)

    # --------------- 画像確認プロセス ---------------
    if left_button.button(
        label="画像確認",
        key="view_image_data",
        type="primary",
        icon=":material/search:",
        use_container_width=True,
    ):
        if len(st.session_state.selected_id_list) == 0:
            st.toast("画像を選択してください", icon="🚨")
        else:
            for image_id in st.session_state.selected_id_list:
                with get_db_session() as db:
                    image_data = get_image_data_by_id(db=db, image_data_id=image_id)

                if image_data is not None:
                    image = Image.open(image_data.file_path)
                    st.image(
                        image,
                        caption=str(image_data.file_name),
                        use_container_width=True,
                    )
                else:
                    st.toast("画像データが見つかりませんでした", icon="🚨")

    # --------------- データ削除プロセス ---------------
    if middle_button.button(
        label="データの削除処理",
        key="delete_image_data",
        type="primary",
        icon=":material/delete:",
        use_container_width=True,
    ):
        if len(st.session_state.selected_id_list) == 0:
            st.toast("画像を選択してください", icon="🚨")
        else:
            with get_db_session() as db:
                delete_image_db_and_folder(
                    db=db, image_id_list=st.session_state["selected_id_list"]
                )
            st.rerun()

    # --------------- 画像処理プロセス ---------------
    if right_button.button(
        label="画像処理",
        key="image_processing",
        type="primary",
        icon=":material/memory:",
        use_container_width=True,
    ):
        if len(st.session_state.selected_id_list) == 0:
            st.toast("画像を選択してください", icon="🚨")
        else:
            progress_bar = st.progress(0, text="画像処理実施中・・・")
            total_images = len(st.session_state.selected_id_list)

            for idx, image_id in enumerate(st.session_state.selected_id_list):
                with get_db_session() as db:
                    image_data = get_image_data_by_id(db=db, image_data_id=image_id)

                if image_data is not None:
                    # 画像処理プロセス
                    image_path = str(image_data.file_path)
                    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

                    if image is None:
                        raise ValueError(
                            f"Failed to read the image from {image_data.file_path}"
                        )

                    processed_image = dummy_heavy_image_processing(image=image)

                    new_file_name = f"processed_{image_data.file_name}"
                    save_path = os.path.join(
                        st.session_state.data_processed_path, new_file_name
                    )
                    cv2.imwrite(save_path, processed_image)
                    st.image(
                        processed_image, caption=new_file_name, use_container_width=True
                    )

                    # データベース処理プロセス
                    # table: processed_image_data
                    processed_data = ProcessedImageDataCreate(
                        file_name=new_file_name,
                        file_path=save_path,
                        processed_at=pd.Timestamp.now(tz="UTC")
                        .tz_convert("Asia/Tokyo")
                        .floor("s"),
                    )
                    with get_db_session() as db:
                        create_processed_image_data(db=db, image_data=processed_data)

                    # table: image_data
                    with get_db_session() as db:
                        update_image_data(
                            db=db, image_data_id=int(image_data.id), is_processed=True
                        )

                else:
                    st.toast("画像データが見つかりませんでした", icon="🚨")
                progress_bar.progress((idx + 1) / total_images)

    if st.button(
        label="AI画像処理",
        key="ai_image_processing",
        type="primary",
        icon=":material/memory:",
    ):
        message_dialog("Maybe comming soon...")
