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

line_bot_api = LineBotApi('ed2RFUJNf34ZE7jAD1f5fsogGVpImDrPwcah8ICrFSDNY1xRdQb4Hc22rF5jlO+w/BI+d2oQpKQ44BbwaNyLIZngw69H2Zt256uz0yr9f6vAN2YYacUyAeD68D32hJ0uIRSnAe87MNS6+Lm5q4UrngdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ddfc324a9605cb8db3b7a4ac64337bd3')


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
