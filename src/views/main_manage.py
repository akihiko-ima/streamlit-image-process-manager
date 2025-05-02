import os
import cv2
import time
import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from PIL import Image
from dotenv import load_dotenv

from services.initialize_setting import initialize_setting
from services.dummy_heavy_image_processing import dummy_heavy_image_processing

# from services.ObjectDetection import ObjectDetection
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
from utils.aggrid_dataframe import configure_aggrid
from utils.image_utils import save_image, delete_image_db_and_folder


def show():
    # --------------- initialized ---------------
    initialize_setting()
    load_dotenv()
    LOG_DIR = os.getenv("LOG_DIR")
    LOG_PATH = os.path.join(LOG_DIR, "line_message.log")

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
                        image, camera_file_name, st.session_state["data_raw_path"], db
                    )

                # 保存をLINEに通知
                message_text = f"画像が保存されました: {camera_file_name}\nURLはこちらです。=> https://imaima-image-process-manager.streamlit.app/"
                send_line_message(
                    USER_ID=st.secrets["LINE_USER_ID"],
                    CHANNEL_ACCESS_TOKEN=st.secrets["LINE_CHANNEL_ACCESS_TOKEN"],
                    messageText=message_text,
                    log_file_path=LOG_PATH,
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
                            st.session_state["data_raw_path"],
                            db,
                        )

                # 保存をLINEに通知
                message_text = f"画像が保存されました: {uploaded_file.name}\nURLはこちらです。=> https://imaima-image-process-manager.streamlit.app/"
                send_line_message(
                    USER_ID=st.secrets["LINE_USER_ID"],
                    CHANNEL_ACCESS_TOKEN=st.secrets["LINE_CHANNEL_ACCESS_TOKEN"],
                    messageText=message_text,
                    log_file_path=LOG_PATH,
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

        df_raw_img["is_processed"] = df_raw_img["is_processed"].apply(
            lambda x: "済" if x else "未"
        )
        df_raw_img = format_datetime_column(df_raw_img, "uploaded_at")
        df_raw_img = format_datetime_column(df_raw_img, "updated_at")

        # データフレームをsession_stateに保存
        if "raw_image_datatable" not in st.session_state:
            st.session_state["raw_image_datatable"] = df_raw_img

        # 選択したデータ情報を取得
        selected_df = configure_aggrid(df_raw_img)
        if not selected_df.empty:
            selected_id_list = selected_df["id"].tolist()
            st.session_state["selected_id_list"] = selected_id_list

    # checkboxを選択していない場合は空リストをセット
    if "selected_id_list" not in st.session_state:
        st.session_state["selected_id_list"] = []

    # --------------- ボタンセクション ---------------
    first_left_button, first_right_button = st.columns(2)

    # --------------- 画像確認プロセス ---------------
    if first_left_button.button(
        label="画像確認",
        key="view_image_data",
        type="primary",
        icon=":material/search:",
        use_container_width=True,
    ):
        if len(st.session_state["selected_id_list"]) == 0:
            st.toast("画像を選択してください", icon="🚨")
        else:
            for image_id in st.session_state["selected_id_list"]:
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
    if first_right_button.button(
        label="データの削除処理",
        key="delete_image_data",
        type="primary",
        icon=":material/delete:",
        use_container_width=True,
    ):
        if len(st.session_state["selected_id_list"]) == 0:
            st.toast("画像を選択してください", icon="🚨")
        else:
            with get_db_session() as db:
                delete_image_db_and_folder(
                    db=db, image_id_list=st.session_state["selected_id_list"]
                )
            st.rerun()

    # --------------- 画像処理プロセス ---------------
    second_left_button, second_right_button = st.columns(2)

    if second_left_button.button(
        label="画像処理",
        key="image_processing",
        type="primary",
        icon=":material/memory:",
        use_container_width=True,
    ):
        if len(st.session_state["selected_id_list"]) == 0:
            st.toast("画像を選択してください", icon="🚨")
        else:
            progress_bar = st.progress(0, text="画像処理実施中・・・")
            total_images = len(st.session_state["selected_id_list"])

            for idx, image_id in enumerate(st.session_state["selected_id_list"]):
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
                        st.session_state["data_processed_path"], new_file_name
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

    if second_right_button.button(
        label="物体検出AI",
        key="ai_image_processing",
        type="primary",
        icon=":material/memory:",
        use_container_width=True,
    ):
        message_dialog("Maybe one day I'll fix it....")

        # if len(st.session_state.selected_id_list) == 0:
        #     st.toast("画像を選択してください", icon="🚨")
        # else:
        #     progress_bar = st.progress(0, text="画像処理実施中・・・")
        #     total_images = len(st.session_state.selected_id_list)

        #     # 物体検出インスタンスを作成
        #     obj_detector = ObjectDetection(model_path="./models/efficientdet_lite0.tflite")

        #     # 結果表示用のst.columns
        #     header_col1, header_col2 = st.columns(2)
        #     header_col1.markdown('#### before')
        #     header_col2.markdown('#### after')

        #     for idx, image_id in enumerate(st.session_state.selected_id_list):
        #         image_data = get_image_data_by_id(db=db, image_data_id=image_id)

        #         if image_data is not None:
        #             image_path = str(image_data.file_path)
        #             image = cv2.imread(image_path)
        #             image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        #             if image is None:
        #                 raise ValueError(
        #                     f"Failed to read the image from {image_data.file_path}"
        #                 )

        #             # 画像認識プロセス
        #             detected_image = obj_detector.process_image(image_file=image_path)
        #             new_file_name = f"ai_processed_{image_data.file_name}"
        #             save_path = os.path.join(
        #                 st.session_state.data_processed_path, new_file_name
        #             )
        #             detected_image_rgb = cv2.cvtColor(detected_image, cv2.COLOR_BGR2RGB)
        #             cv2.imwrite(save_path, detected_image_rgb)

        #             # 結果表示
        #             col_1, col_2 = st.columns(2)
        #             with col_1:
        #                 st.image(image_rgb, use_container_width=True)
        #             with col_2:
        #                 st.image(detected_image, caption=new_file_name, use_container_width=True)

        #             # データベース処理プロセス
        #             processed_data = ProcessedImageDataCreate(
        #                 file_name=new_file_name,
        #                 file_path=save_path,
        #                 processed_at=pd.Timestamp.now(tz="UTC")
        #                 .tz_convert("Asia/Tokyo")
        #                 .floor("s"),
        #             )
        #             create_processed_image_data(db=db, image_data=processed_data)

        #             # table: image_data
        #             update_image_data(
        #                 db=db, image_data_id=int(image_data.id), is_processed=True
        #             )
        #         else:
        #             st.toast("画像データが見つかりませんでした", icon="🚨")

        #         progress_bar.progress((idx + 1) / total_images)

    if st.button(
        label="somthing",
        key="somthing",
        type="primary",
    ):
        message_dialog("Maybe something is coming soon...")
