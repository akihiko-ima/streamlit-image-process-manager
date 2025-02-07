import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session

from services.initialize_setting import initialize_setting
from database.database import get_db_session
from database.models import Comment


def show():
    initialize_setting()

    st.title(":material/identity_platform: コメントログ機能")
    comment = st.text_input("コメントを入力してください")
    if st.button(
        label="コメントを保存",
        key="add_comment",
        type="primary",
        icon=":material/chat:",
    ):
        if comment:
            with get_db_session() as db:
                new_comment = Comment(
                    content=comment, created_at=pd.Timestamp.now().floor("s")
                )
                db.add(new_comment)
                db.commit()
                db.refresh(new_comment)
                print(f"{new_comment.content}: comment at {new_comment.created_at}")
                st.toast("コメントが保存されました！", icon="🎉")
        else:
            st.error("コメントを入力してください。")
