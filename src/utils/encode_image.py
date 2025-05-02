import base64


def encode_image(file_path):
    try:
        with open(file_path, "rb") as f:
            return f"data:image/png;base64,{base64.b64encode(f.read()).decode('utf-8')}"
    except FileNotFoundError:
        return None  # ファイルが存在しない場合
