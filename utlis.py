from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from time import sleep

driver = webdriver.Chrome()
driver.get('https://web.whatsapp.com/')
qr = False
while not qr:
    if 'To use WhatsApp on your computer:' in driver.page_source:
        qr = True
        sleep(2)
        driver.save_screenshot('QR/qr.png')

input('enter after QR scan')


def send(phone_no, msg):
    driver.get('https://web.whatsapp.com/send?phone={}&text={}'.format(phone_no, msg))
    x = False
    while not x:
        if msg in driver.page_source:
            x = True
    active_element = driver.switch_to.active_element
    active_element.send_keys(Keys.RETURN)
    sleep(1)

# import pickle
# pickle.dump( driver.get_cookies() , open("cookies.pkl","wb"))
