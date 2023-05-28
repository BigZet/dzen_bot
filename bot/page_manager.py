from datetime import datetime
from pathlib import Path
import logging
import re

class PageManager:
    def __init__(self, driver, pagePath):
        self.logger = logging.getLogger(__name__)
        self.driver = driver
        self.pagePath = pagePath

    def go(self, url):
        self.logger.debug(f"Go to page: {url}")
        self.url = url
        self.page_content = self.driver.goToPage(self.url)
        self.savePage()
        self.driver.randomSleep(8)

    def savePage(self):
        self.logger.debug(f"Save page: {self.url}")
        self.lastPageName = datetime.today().strftime('%Y%m%d%H%M%S') + "_" + re.sub('[^A-Za-z0-9]', '#', re.sub('(https|http)(:)*|(\/)*', '', self.url))
        Path(self.pagePath, self.lastPageName).mkdir(parents=True, exist_ok=True)
        self.lastPageFilePath = Path(self.pagePath, self.lastPageName, 'index.html')
        self.lastPageImagePath = Path(self.pagePath, self.lastPageName, 'image.png')

        self.logger.debug(f"Save html: {self.lastPageFilePath}")
        with open(self.lastPageFilePath, "w", encoding="utf-8") as f:
            f.write(self.page_content)
        self.logger.debug(f"Save image: {self.lastPageImagePath}")
        self.driver.takeScreen(self.lastPageImagePath)
        

    def test(self):
        self.go("https://bot.sannysoft.com/")
        
        
    