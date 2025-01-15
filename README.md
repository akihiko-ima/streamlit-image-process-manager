# Python version 3.11.9

## 実行環境
このアプリはubuntu環境でのみ実行します。
(mediapipe0.10.20とstreamlitの組み合わせではエラーが生じる可能性があります。)

## 採用技術

- **フロントエンド**: Streamlit
- **ORM**: SQLAlchemy
- **データベース**: SQLite
- **デザイン**: Material Design Icons
- **画像処理**: OpenCV

## アーキテクチャ

![アーキテクチャ](docs/ST-IPM-architecture.png)

## GIF

How to use this application.

<img src="./docs/sample_video.gif" alt="sample" style="height:500px;">

## Directory structure

```bash
streamlit-image-process-manager/
├─ .streamlit/                             # streamlit標準config
│  └─ config.toml
├─ data/                                   # 画像保存先
│  ├─ processed/
│  └─ raw/
├─ database/                               # データベース設定
│  ├─ cruds/
│  │  ├─ image_data.py
│  │  └─ processed_image_data.py
│  ├─ database.py
│  └─ models.py
├─ schemas/                                # スキーマdirectory
│  └─ schemas.py
├─ services/                               # フロントエンドから呼び出す関数を保存
│  ├─ delete_image_data.py
│  ├─ dummy_heavy_image_processing.py
│  └─ initialize_setting.py
├─ utils/                                  # 汎用関数
│  └─ format_datetime_column.py
├─ pages/
│  ├─ 1_🚀_processed_check_page.py
│  ├─ 2_📑_bonus_comment_page.py
│  └─ 3_⚠️_README.py
├─ .env                                    # 環境設定
├─ app.py                                  # メインアプリケーション
└─ data.db                                 # データベース(SQLite)
```

## アプリの実行

- app 起動</br>
  streamlit run app.py

- 仮想環境作成</br>
  => python3 -m venv env_st_app

- 仮想環境起動</br>
  => source ./env_st_app/bin/activate

- requirements.txt</br>
  pip install -r requirements.txt</br>
  pip freeze > requirements.txt</br>
