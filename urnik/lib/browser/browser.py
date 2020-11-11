"""
    Downloads the data of the URL: http://wise-tt.com/wtt_um_feri/

    The entire browser process is done by using Selenium and Firefox

"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options

import time
import os
import sys
import logging


class Browser:
    browser = None
    destination = None

    sleep = 2

    def __init__(self, destination):
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)  # Browser will download to "browser.browser.dir"
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", destination)  # TODO: change None .ini settings
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/octet-stream, text/calendar,application/vnd.sus-calendar,text/x-vcalendar")

        options = Options()
       #  options.add_argument("--headless")  # Hide browser window

        self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        self.destination = destination

    def download_schedule(self, url):
        self.browser.get(url)

        wait = WebDriverWait(self.browser, 4)

        logging.info("The browser is loading the site")
        time.sleep(self.sleep)

        script = """return $("span:contains('iCal-teden')").parent()["""
        download_button_id = self.browser.execute_script(script + "0].id")
        if download_button_id == "":
            download_button_id = self.browser.execute_script(script + "1].id")

        element_type = wait.until(EC.element_to_be_clickable((By.ID, download_button_id)))
        element_type.click()

        # A basic progress bar loop till the file has downloaded
        for i in range(1, 10):

            # Checks if the file hasn't been downloaded in in the directory self.downloadPath
            if (not any("calendar" in file for file in
                        os.listdir(self.destination))):  # TODO: fix the download path problem, which should be get
                time.sleep(0.4)
                sys.stdout.write("\rDownloading {}".format("." * i))
                sys.stdout.flush()
            else:
                print("\nDownloaded file.")
                break

        self.browser.quit()
