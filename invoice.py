#linebotTest1
# ngrok http 5000
import random
import clawer
import re
from flask import Flask, request , abort
app = Flask(__name__)

from linebot import  LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage, StickerSendMessage, LocationSendMessage, QuickReply,QuickReplyButton, MessageAction
line_bot_api = LineBotApi('k/HVDioE+/cG+b24V2c0vLvYbe1CgtmVo5uAz3IDyC3MwwhRRUxqUrbGFwjiuW4seNE37jTFUdYGgQB+Zv9UJEkt4HchRR4mhwQSEhnJqVknTz/qHiYfCInpoQjg7JjFDrb7lq0Mh1M7V8ngDbiOfgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('ff0138a40953ad704412fb621ebbee64')


@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    #獲得使用者輸入的訊息
    body = request.get_data(as_text = True)
    try:
        #送出
        handler.handle(body,signature)
    except InvalidSignatureError:
        #送出 Bad request (400)
        abrot(400)
    #回覆OK
    return 'ok'

@handler.add(MessageEvent, message = TextMessage)
# 加入一個 handle_message function
def handle_message(event):
    input_text = event.message.text
    if input_text == "@本期中獎號碼":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = clawer.askPrize(0)))
    if input_text == "@前期中獎號碼":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = clawer.askPrize(1)))
    if input_text == "獎金":
        line_bot_api.reply_message(event.reply_token,TextSendMessage(text = clawer.PRIZE))
    else:
        number = re.sub("\D","",input_text)
        if number != "" and len(number) == 3:
            (isWin,content) = clawer.checkWinPrize(number)
            # 0 - 沒中， 1 當期有中 , 2 前期有中
            if isWin:
                try:
                    message = [
                    TextSendMessage(text=content),
                    TextSendMessage(text = clawer.askPrize(isWin-1))
                    ]
                    line_bot_api.reply_message(event.reply_token, message)
                except:
                    line_bot_api.reply_message(event.reply_token,TextSendMessage(text="error!"))    
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text = content))
        else:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text = "輸入三個數字讓我看看你有沒有發達!"))
     

if __name__ == '__main__':
    app.run()