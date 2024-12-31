import streamlit as st


st.title("アプリの解説")

st.subheader(":material/info: 概要", divider=True)
st.markdown(
    """
#### 画像アップロード:
ユーザーが画像ファイルをアップロードし、データベースに保存することができます。

#### データベース管理:
アップロードされた画像データをデータベースに保存し、データベース内の画像データを表示・編集・削除することができます。

#### コメントログ機能:
ユーザーがコメントを入力し、データベースに保存することができます。
"""
)
st.write("")

st.subheader(":material/warning: 注意事項", divider=True)
st.markdown(
    """
・当アプリの利用により生じたいかなる損害についても、開発者は責任を負いかねます。アプリのご利用にあたっては、上記の注意事項をご理解いただいたものとみなします。
"""
)
st.write("")

st.subheader(":material/manufacturing: 採用技術", divider=True)
st.markdown(
    """
- **フロントエンド**: Streamlit
- **ORM**: SQLAlchemy
- **データベース**: SQLite
- **デザイン**: Material Design Icons
- **画像処理**: OpenCV
    """
)
st.write("")
st.image("./docs/ST-IPM-architecture.png", use_container_width=True)
