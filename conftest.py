import logging
import os
import pathlib
import time

import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def pytest_configure(config):
    """Configure logging for the test session."""
    logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s", level=logging.INFO
    )
    logging.getLogger("selenium").setLevel(logging.INFO)
    logging.info("Logging configured for pytest session")


@pytest.fixture(autouse=True)
def log_test_start_and_end(request):
    """Logs before and after each test."""
    logger = logging.getLogger(request.node.name)
    logger.info(f"STARTING TEST: {request.node.name}")
    yield
    logger.info(f"FINISHED TEST: {request.node.name}")


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("HUDL_BASE_URL", "https://hudl.com")


@pytest.fixture(scope="session")
def creds():
    return {
        "email": os.getenv("HUDL_EMAIL", ""),
        "password": os.getenv("HUDL_PASSWORD", ""),
    }


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--window-size=1366,876")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    yield driver
    driver.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        driver = item.funcargs.get("driver", None)
        if driver:
            pathlib.Path("screenshots").mkdir(exist_ok=True)
            filename = f"screenshots/{item.name}_{int(time.time())}.png"
            driver.save_screenshot(filename)
