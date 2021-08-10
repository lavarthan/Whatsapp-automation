import sys
from flask import Flask, Response
from flask import request
import logging
# from utlis import send
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

app = Flask(__name__)
app.logger.addHandler(logging.StreamHandler(sys.stdout))
app.logger.setLevel(logging.ERROR)

options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--headless')
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)
driver.get('https://web.whatsapp.com/')
print('driver launched..')
# qr = False
# while not qr:
#     if 'To use WhatsApp on your computer:' in driver.page_source:
#         qr = True
#         sleep(2)
#         driver.save_screenshot('static/img.jpg')


def send(phone_no, msg):
    driver.get('https://web.whatsapp.com/send?phone={}&text={}'.format(phone_no, msg))
    x = False
    while not x:
        if msg in driver.page_source:
            x = True
    active_element = driver.switch_to.active_element
    active_element.send_keys(Keys.RETURN)
    sleep(1)


@app.route('/', methods=['GET'])
def home():
    driver.get('https://web.whatsapp.com/')
    sleep(2)
    if 'To use WhatsApp on your computer:' in driver.page_source:
        return '''<b>scan QR code<b> <br><img src="/static/img.png" coords="1110,192,1458,533">'''
    else:
        return 'You already logged in!!!'


@app.route('/send_sms', methods=['GET'])
def send_sms():
    phone_no = request.args.get('mobile')
    msg = request.args.get('message')
    token = request.args.get('token')

    if token == '123456':
        send(phone_no, msg)
        return 'Successfully message sent'


if __name__ == '__main__':
    app.debug = True
    app.run(use_reloader=False, threaded=True)
