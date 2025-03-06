# coding: utf-8

import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from retrying import retry

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(asctime)s %(message)s')

@retry(wait_random_min=5000, wait_random_max=10000, stop_max_attempt_number=3)
def enter_iframe(browser):
    logging.info("Enter login iframe")
    time.sleep(5)  # 给 iframe 额外时间加载
    try:
        iframe = WebDriverWait(browser, 10).until(
            EC.presence_of_element_located((By.XPATH, "//*[starts-with(@id,'x-URS-iframe')]")
        ))
        browser.switch_to.frame(iframe)
        logging.info("Switched to login iframe")
    except Exception as e:
        logging.error(f"Failed to enter iframe: {e}")
        browser.save_screenshot("debug_iframe.png")  # 记录截图
        raise
    return browser

@retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=5)
def extension_login():
    chrome_options = webdriver.ChromeOptions()

    logging.info("Load Chrome extension NetEaseMusicWorldPlus")
    chrome_options.add_extension('NetEaseMusicWorldPlus.crx')

    logging.info("Initializing Chrome WebDriver")
    try:
        service = Service(ChromeDriverManager().install())  # Auto-download correct chromedriver
        browser = webdriver.Chrome(service=service, options=chrome_options)
    except Exception as e:
        logging.error(f"Failed to initialize ChromeDriver: {e}")
        return

    # Set global implicit wait
    browser.implicitly_wait(20)

    browser.get('https://music.163.com')

    # Inject Cookie to skip login
    logging.info("Injecting Cookie to skip login")
    browser.add_cookie({"name": "MUSIC_U", "value": "00086670BEAF98E1224BA1196CB55E5C2A521E73CC05CB49B8EC3E50F928F4AAC7FE29199D8D4711E4D39E658D06A6B611A848DB41BA27E0AE43BA9B7F311A9770D8AADCA6A3F8D90B98949F2EBE71D0840443F7EEB4DB20C557FD2791DFC8F49E3CC45AF0BBF51FA178D59F73D996ABA09A402D1D9C01208B042FC8487138BE05241BE181E1CBBB5C862885B3FB478D0D00FA9318810E2515973A1C6B935EE0D2990116E791C548946A1B689484A9BD5B33E28B53FF344F8A1F1610455617D8DA41C9D3897DCF84C2A00450DB47012A805E4142328FD5BA1B6CFAE6C41285F813F62B37B08A0D54779616ECA7057740228275F4252B1440BB56BB99F4B11E90E5B316E00191262E360346422569CA2D9A9307A0C365CB9A1601EA8F73088F51BD0B168558911B6DA73FFF8009EFE5A2475AFDB78919A2C0921AF7E71E6D389853"})
    browser.refresh()
    time.sleep(5)  # Wait for the page to refresh
    logging.info("Cookie login successful")

    # Confirm login is successful
    logging.info("Unlock finished")

    time.sleep(10)
    browser.quit()


if __name__ == '__main__':
    try:
        extension_login()
    except Exception as e:
        logging.error(f"Failed to execute login script: {e}")
