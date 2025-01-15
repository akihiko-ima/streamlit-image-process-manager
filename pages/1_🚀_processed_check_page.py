import streamlit as st
import cv2
import pandas as pd
from PIL import Image
from sqlalchemy.orm import Session
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from services.initialize_setting import initialize_setting
from database.database import get_db
from database.cruds.processed_image_data import (
    get_all_processed_images,
    get_processed_image_data_by_id,
)
from utils.format_datetime_column import format_datetime_column

# --------------- initialized ---------------
initialize_setting()
st.set_page_config(
    page_title="Image Process Manager", page_icon=":camera:", layout="wide"
)
db: Session = next(get_db())


st.title(":material/folder_managed: 画像処理結果確認")

processed_image_data_list = get_all_processed_images(db=db)

# データフレームの作成
if len(processed_image_data_list) > 0:
    df_processed_img = pd.DataFrame(processed_image_data_list)
    df_processed_img = format_datetime_column(df_processed_img, "processed_at")

    # AgGridのsetting
    grid_builder = GridOptionsBuilder.from_dataframe(
        df_processed_img, editable=False, filter=True, resizable=True, sortable=False
    )
    grid_builder.configure_selection(selection_mode="multiple", use_checkbox=True)
    grid_builder.configure_side_bar(filters_panel=True, columns_panel=False)
    grid_builder.configure_default_column(
        enablePivot=True, enableValue=True, enableRowGroup=True
    )
    grid_builder.configure_grid_options(rowHeight=50)
    grid_options = grid_builder.build()
    grid_options["columnDefs"][0]["checkboxSelection"] = True

    response = AgGrid(
        df_processed_img,
        gridOptions=grid_options,
        update_mode=GridUpdateMode.MODEL_CHANGED,
        theme="alpine",
    )

    # ユーザーが選択したデータ情報を取得
    selected_df = pd.DataFrame(response["selected_rows"])
    if not selected_df.empty:
        selected_processed_id_list = selected_df["id"].tolist()
        st.session_state.selected_processed_id_list = selected_processed_id_list

# checkboxを選択していない場合は空リストをセット
if "selected_processed_id_list" not in st.session_state:
    st.session_state.selected_processed_id_list = []

if st.button(
    label="画像処理結果確認",
    key="view_processed_image_data",
    type="primary",
    icon=":material/search:",
):
    if len(st.session_state.selected_processed_id_list) == 0:
        st.toast("画像を選択してください", icon="🚨")
    else:
        for image_id in st.session_state.selected_processed_id_list:
            image_data = get_processed_image_data_by_id(db=db, image_id=image_id)

            if image_data is not None:
                image = cv2.imread(image_data.file_path)
                image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                st.image(
                    image_rgb, caption=str(image_data.file_name), use_container_width=True
                )
            else:
                st.toast("画像データが見つかりませんでした", icon="🚨")
