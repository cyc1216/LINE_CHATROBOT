from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('BHihGszKfHim83P4zQ+CQ3g5ToKV5mrp9qwQkeqCQZoL3UAeSdO7Rvt1yl3sWdlx5ZLFwP8p2WeMzTewDUkm3xYzKCF2PVvTnyCPaWYfTaSmLqpR7uSkRsWORIpxKsx5YlrlfTPVuY2zqa8fa97gkAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('0a8fd0a63e043d42054ca1cae62829e7')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()