"""
    Downloads the data of the URL: http://wise-tt.com/wtt_um_feri/

    The entire browser process is done by using Selenium and Firefox

"""
import time
import os
import sys
import glob

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.options import Options


class Browser:
    browser = None
    destination = None

    sleep = 2

    def __init__(self, destination: str, hide_browser=True) -> None:
        """
        A Browser class used for accessing the website from which it download the .ics file or schedule.

        Uses the 'geckodriver' browser web engine.

        @param destination: Folder path where the browsers saves downloaded files.
        @param hide_browser: Should the object display the browser. Useful for debugging.
        """
        profile = webdriver.FirefoxProfile()
        profile.set_preference("browser.download.folderList", 2)  # Browser will download to "browser.browser.dir"
        profile.set_preference("browser.download.manager.showWhenStarting", False)
        profile.set_preference("browser.download.dir", destination)
        profile.set_preference("browser.helperApps.neverAsk.saveToDisk",
                               "application/octet-stream, text/calendar,application/vnd.sus-calendar,text/x-vcalendar")

        options = Options()
        if hide_browser:
            options.add_argument("--headless")  # Hide browser window

        self.browser = webdriver.Firefox(firefox_profile=profile, firefox_options=options)
        self.destination = destination

    def download_schedule(self, url: str) -> None:
        """
        Download the .ics file from the site using the url parameter.

        @param url: Url of the site to download from
        """

        # First removes any ics file specified in the destination folder
        for i in glob.iglob(str(self.destination) + "/*.ics"):
            os.remove(i)

        self.browser.get(url)

        wait = WebDriverWait(self.browser, 4)

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
                        os.listdir(self.destination))):
                time.sleep(0.4)
                sys.stdout.write("\rDownloading {}".format("." * i))
                sys.stdout.flush()
            else:
                print("\nDownloaded file.")
                break

        self.browser.quit()
