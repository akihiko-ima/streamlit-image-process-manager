import requests
import logging


def setup_logging(log_file_path: str):
    logging.basicConfig(
        filename=log_file_path,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        encoding="utf-8",
    )


def send_line_message(
    USER_ID: str, CHANNEL_ACCESS_TOKEN: str, messageText: str, log_file_path: str
):
    setup_logging(log_file_path)
    headers = {
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }
    url = "https://api.line.me/v2/bot/message/push"
    data = {"to": USER_ID, "messages": [{"type": "text", "text": messageText}]}

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        logging.info(f"メッセージが送信されました: {messageText}")
    else:
        logging.error(f"エラーが発生しました: {response.status_code}, {response.text}")


