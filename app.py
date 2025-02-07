import streamlit as st
from sqlalchemy.orm import Session

from router import router
from services.initialize_setting import initialize_setting
from database.database import get_db


st.set_page_config(
    page_title="Image Process Manager", page_icon=":camera:", layout="wide"
)
initialize_setting()

db: Session = next(get_db())

router()
