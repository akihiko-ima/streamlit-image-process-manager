import os
import streamlit as st
from dotenv import load_dotenv

from database.database import create_tables


def initialize_setting():
    """
    環境設定を初期化する関数。

    .envファイルを読み込み、必要なディレクトリを作成し、
    Streamlitのsession_stateにパスを設定します。

    Raises:
        OSError: ディレクトリの作成に失敗した場合に発生します。
    """
    load_dotenv()

    if "is_initialized" not in st.session_state:
        st.session_state["is_initialized"] = False

    if not st.session_state["is_initialized"]:
        DATA_PATH = os.getenv("DATA_PATH")
        DATA_RAW_PATH = os.path.join(DATA_PATH, "raw")
        DATA_PROCESSED_PATH = os.path.join(DATA_PATH, "processed")
        LOG_DIR = os.getenv("LOG_DIR")

        if DATA_PATH and not os.path.exists(DATA_PATH):
            os.makedirs(DATA_PATH)
            os.makedirs(DATA_RAW_PATH)
            os.makedirs(DATA_PROCESSED_PATH)
            os.makedirs(LOG_DIR)

            print(f"Directory created.")
        else:
            print(f"Directory already exists or DIR_PATH is not set in .env file.")

        create_tables()

        # session_stateの設定
        if "db_path" not in st.session_state:
            st.session_state["db_path"] = os.getenv("DB_PATH")
        if "data_raw_path" not in st.session_state:
            st.session_state["data_raw_path"] = DATA_RAW_PATH
        if "data_processed_path" not in st.session_state:
            st.session_state["data_processed_path"] = DATA_PROCESSED_PATH
        if "selected_id_list" not in st.session_state:
            st.session_state["selected_id_list"] = []

        st.session_state["is_initialized"] = True

    # CSSでst.toastのスタイルをカスタマイズ
    st.markdown(
        """
        <style>
        .stToast {
            background-color: #64748b !important;
            color: white !important;
            border-radius: 10px;
            padding: 18px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
