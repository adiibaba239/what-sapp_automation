
import time

import subprocess
import random
from selenium import webdriver

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



def open_whatsapp_in_chrome():
    try:
        port = random.randint(9000, 9999)
        chrome_path = input("Enter Chrome path and leave empty for default path: ")
        if not chrome_path:
            chrome_path = r'C:\Program Files\Google\Chrome\Application\chrome.exe'
        subprocess.Popen([chrome_path, f'--remote-debugging-port={port}', 'https://web.whatsapp.com'])
        time.sleep(10)

        chrome_options = webdriver.ChromeOptions()
        chrome_options.debugger_address = f"127.0.0.1:{port}"
        driver = webdriver.Chrome(options=chrome_options)

        wait = WebDriverWait(driver, 30)
        wait.until(EC.title_contains("WhatsApp"))

        return driver, port
    except Exception as e:
        print(f"Error opening WhatsApp in Chrome: {str(e)}")
        return None, None
