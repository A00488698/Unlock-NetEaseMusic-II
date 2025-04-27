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
    browser.add_cookie({"name": "MUSIC_U", "value": "0091CD74E70CF1FBD32850A28A29016C65D707627CCF3F4EC175F5227EF506DBEFF497E6297E8D942F0B48D36154E625589D27AA3052F86A8ADE31ADF0CDDD1F503C58FD5669093092919C99547E413A45700E06403F6DE326F6F2BAF17B1CD933E524C42EB65FE50CBBD490D79A944DE95D35AFC719038D7A4144154B3C5431DAA8BFB21748B7938486B756843DBDB3ADC4CC872CB30C0A02DF14008C24927E82C05B92C05609460251D01DA8C71E288909BE02DBF099373B1978B806C27031240F90A209AE235DF6FBBC4CAB08B879B8BFCF9D648EEBDA5358E4E550289003C7C36E7C4A342918FAAEC9560D27B810477D03D3E6DE83F0F531EA595A9657693AE668A62DA36CB68524506D25F7BC1A105CAAB7E67757DB0E9011570F19AD310977B8987CD950424B7F195AE4DDB5977535F50B4433373F8D543148C96B158554E8A0E7F0248B248B6A9C60DD5A42D9BAEC79D3432A629C1E02D1568698F6FB96"})
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
