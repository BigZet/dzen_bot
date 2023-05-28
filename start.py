import logging.config
from pathlib import Path
import argparse
import yaml
import time

from bot import drivers
from bot import utils
from bot import page_manager



def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--logger_config_path", "-lc", type=str, default="configs\logger.conf", help="Path for logger config file")
    parser.add_argument("--driver_config_path", "-dc", type=str, default="configs\driver.yaml", help="Path for driver config file")
    args, _ = parser.parse_known_args()
    
    logger_config_path = Path(args.logger_config_path)
    assert logger_config_path.exists(), "Cannot find logger config file"
    logging.config.fileConfig(logger_config_path)
    logger = logging.getLogger(__name__)

    logger.debug("Application start")

    driver_config_path = Path(args.driver_config_path)
    assert driver_config_path.exists(), logger.error("Cannot find driver config file")

    with open(driver_config_path, 'r') as f:
        driver_config = yaml.safe_load(f.read())
    
    logger.debug("Loaded driver config: " + str(driver_config))

    driver_config = utils.make_browser_config(driver_config)

    logger.debug("Succesfully parsed driver config: " + str(driver_config))

    if driver_config.get("engine") == "chrome":
        driver =  drivers.ChromeDriver(driver_config)

    pm = page_manager.PageManager(driver, driver_config.get('pages_path'))
    pm.test()
    for i in ["https://www.google.com/", "https://yandex.com/", "https://www.bing.com/", "https://www.yahoo.com/"]:
        pm.go(i)

    driver.quit()
    logger.debug("Closing driver")
    logging.shutdown()

if __name__ == '__main__':
    main()

    