from selenium import webdriver
from selenium_stealth import stealth
from fake_useragent import UserAgent
import logging

class Driver:
    def __init__(self,  config, engine):
        self.engine = engine
        self.logger = logging.getLogger(__name__)
        self.config = config
        self.driver = self.getDriver()

        if self.config['stealth']:
            self.enableStealth()
    
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
            self.driver,
            **stealth_config 
        )
    
    def restart_driver(self, config = None):
        self.logger.debug(f"Reloading driver")
        self.driver.quit()

        if config:
            self.config = config
        self.driver = self.getDriver()
        if self.config['stealth']:
            self.enableStealth()

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
