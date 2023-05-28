from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

from selenium_stealth import stealth
from time import sleep
import traceback

import numpy as np
from fake_useragent import UserAgent
import logging
from pathlib import Path

class Driver:
    def __init__(self,  config, engine):
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.webdriver = self.getDriver()

        if self.config['stealth']:
            self.enableStealth()

        if self.config.get("implicit_wait"):
            webdriver.implicitly_wait(self.config.get("implicit_wait"))
    
    def getDriver(self):
        self.logger.debug(f"Init {self.engine}: {self.config}")

    def getConf(self):
        return self.config
    
    def enableStealth(self):
        stealth_args = [
            "languages", "vendor", "platform", 
            "webgl_vendor", "renderer", "fix_hairline"
            ]
        if "user-agent" in self.config.keys():
            stealth_args.append("user-agent")
        stealth_config = dict(zip(stealth_args, map(self.config.get, stealth_args)))
        self.logger.debug(f"Enable stealth mode: {stealth_config}")
        stealth(
            self.webdriver,
            **stealth_config 
        )
    
    def restart_driver(self, config = None):
        self.logger.debug(f"Reloading driver")
        self.webdriver.quit()

        if config:
            self.config = config
        self.webdriver = self.getDriver()
        if self.config['stealth']:
            self.enableStealth()

    def randomSleep(self, loc = 5, scale = 2):
        sleep_secs = np.random.normal(loc, scale)
        self.logger.debug(f"Sleep secs {sleep_secs}")
        sleep(sleep_secs)


    def goToPage(self, url, timeout = 60, waitElementID = None, waitScript = True):
        
        self.webdriver.get(url)
        if waitElementID:
            try:
                self.logger.debug(f"Page load element waiting: {waitElementID}")
                element_present = EC.presence_of_element_located((By.ID, waitElementID))
                WebDriverWait(self.webdriver, timeout).until(element_present)
            except TimeoutException:
                self.logger.error("Timed out waiting for page to load")
                return None
        elif waitScript:
            self.logger.debug(f"Page load script waiting")
            page_load_timeout = timeout
            while (self.webdriver.execute_script('return document.readyState;') != "complete"):
                if page_load_timeout <= 0:
                    self.logger.error("Timed out waiting for page to load")
                    return None
                page_load_timeout -= 5
                self.randomSleep(5)
        return self.webdriver.page_source
    
    def takeScreen(self, path):
        try:
            self.webdriver.find_element(By.TAG_NAME, 'body').screenshot(str(path))
        except Exception as e:
            logging.error(traceback.format_exc())
    def quit(self):
        self.webdriver.quit()


class ChromeDriver(Driver):
    def __init__(self, config):
        super().__init__(config, "ChromeDriver")
        
    def getDriver(self):
        super().getDriver()
        options = webdriver.ChromeOptions()
        if self.config.get('start_maximized'): options.add_argument("start-maximized")
        if self.config.get('headless'): options.add_argument("--headless")
        options.add_experimental_option("excludeSwitches", self.config.get('excludeSwitches'))
        options.add_experimental_option('useAutomationExtension', self.config.get('useAutomationExtension'))
        return webdriver.Chrome(options=options, executable_path=self.config.get('driver_path'))
