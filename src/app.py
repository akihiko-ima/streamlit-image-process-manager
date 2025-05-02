import streamlit as st

from router import router
from services.initialize_setting import initialize_setting


st.set_page_config(
    page_title="Image Process Manager", page_icon=":camera:", layout="wide"
)

initialize_setting()

router()
