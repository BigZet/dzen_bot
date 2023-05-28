from fake_useragent import UserAgent
from pathlib import Path
import logging
import os


DEFAULT_CONFIG = {
    "engine": "chrome",
    "headless": False,
    "start_maximized": True,
    "excludeSwitches": ["enable-automation"],
    "languages":["en-US", "en"],
    "useAutomationExtension": False,
    "vendor": "Google Inc.",
    "platform": "Win32",
    "webgl_vendor": "Intel Inc.",
    "renderer":"Intel Iris OpenGL Engine",
    "fix_hairline":True,
    "pages_path": "pages",
    "stealth": True
}





def make_browser_config(config):
    logger = logging.getLogger(__name__)
    for key in set(list(DEFAULT_CONFIG.keys()) + list(config.keys())):
        config[key] = next((i for i in [config.get(key), DEFAULT_CONFIG.get(key)] if i is not None), None)
        if key == "user_agent":
            if config[key] == "random":
                config[key] = UserAgent().random
            elif config[key] == "chrome":
                config[key] = UserAgent().chrome
        if "path" in key:
            config[key] = Path(config[key])
            if not config[key].exists():
                logger.error(f"Cannot find {key}: {config[key]}")
                raise RuntimeError(f"Cannot find {key}: {config[key]}")
    return config

            

