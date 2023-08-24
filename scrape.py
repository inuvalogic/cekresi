#!/usr/bin/env python3

import time
import datetime
import re
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def contains_date(string):
    date_pattern = r'\d{2}-\d{2}-\d{4}'
    return re.search(date_pattern, string) is not None

def checkResi(noresi):
    try:
        chrome_driver_path = '/usr/bin/chromedriver'
        
        service = Service(chrome_driver_path)

        options = Options()
        # options.add_argument('--headless')
        options.add_argument('user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36')
        
        with webdriver.Chrome(service=service, options=options) as driver:

            driver.maximize_window()
            
            webURL = f"https://cekresi.com/"

            print(f"checking no resi {noresi} ...")
            driver.get(webURL)

            time.sleep(2)

            wait = WebDriverWait(driver, 100)
            noresi_path = '//input[@type="text"][@id="noresi"][@name="noresi"]'
            noresi_form = wait.until(EC.presence_of_element_located((By.XPATH, noresi_path)))
            noresi_form.send_keys(noresi)

            button_path = '//button[@id="cekresi"][contains(text(),"CEK RESI")]'
            button_form = wait.until(EC.presence_of_element_located((By.XPATH, button_path)))
            button_form.click()

            button_jne_path = '//div[@id="selexpid"]//div[@class="hideContent"]//a[contains(text(),"JNE")]'
            button_jne_form = wait.until(EC.presence_of_element_located((By.XPATH, button_jne_path)))
            button_jne_form.click()

            time.sleep(2)

            tracking_path = '//div[@id="results"]//a[contains(@class,"accordion-toggle")][contains(text(), "Lihat perjalanan paket")]'
            tracking_form = wait.until(EC.presence_of_element_located((By.XPATH, tracking_path)))
            tracking_form.click()

            time.sleep(2)

            tabletracking_path = '//div[@id="collapseTwo"]//table[@class="table"]//tbody'
            tracking_table = wait.until(EC.presence_of_element_located((By.XPATH, tabletracking_path)))
            
            output = []

            for row in tracking_table.find_elements(By.TAG_NAME, 'tr'):
                td = row.find_elements(By.TAG_NAME, 'td')
                items = {}
                for item in td:
                    if contains_date(item.text):
                        items['date'] = item.text
                    else:
                        items['desc'] = item.text
                output.append(items)

            driver.quit()

            return output

    except Exception:
        output = {
            'error': f"tidak ada data untuk no resi {noresi}"
        }
        return output

resi_list = {
    'TLJR3DWDMNMPQEDR',
}

for resi in resi_list:
    track = checkResi(resi)
    print(track)
