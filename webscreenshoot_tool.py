#!/usr/bin/env python3

from genericpath import isdir
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime, timezone
from os import path, mkdir

def clean_up(browser, display):
    browser.quit()
    display.stop()

def ab(browser, display):
    try:
        WebDriverWait(browser, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "message-component.message-button.no-children.focusable.sp_choice_type_11"))).click()
    except Exception as e:
        print("Could not click", e)
        clean_up(browser, display)
        pass
def folderlogic(folder):
    if path.isdir(folder):
        return
    else:
        try:
            mkdir(folder)
        except:
            print("Critical: Could not create folder")
            exit(1)

def main():
    d = datetime.now(timezone.utc)
    day = f"{d.strftime('%Y%m%d')}"
    tod = f"{d.strftime('%H%M%S')}"
    hostname = "svt.se"
    rootfolder = "/data/mounts/archive/webscrape"
    folderlogic(f"{rootfolder}/{hostname}/{day}")
    filename = f"{day}.{tod}.png"
    display = Display(visible=0, size=(1080, 3000))
    display.start()
    browser = webdriver.Firefox()
    browser.set_window_size(1080, 3000)
    browser.get(f"https://{hostname}")
    browser.save_screenshot(f"{rootfolder}/{hostname}/{day}/{filename}")
    clean_up(browser, display)

if __name__ == '__main__':
        main()

