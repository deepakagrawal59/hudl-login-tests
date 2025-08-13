from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LandingPage:

    LOGIN_TRIGGER = (By.CSS_SELECTOR, "[data-qa-id='login-select']")
    HUDL_LOGIN_LINK = (By.CSS_SELECTOR, "[data-qa-id='login-hudl']")
    HUDL_LOGO = (By.CSS_SELECTOR, "img[src*='hudl_icon']")

    def __init__(self, driver, base_url, timeout=10):
        self.driver = driver
        self.base_url = base_url
        self.wait = WebDriverWait(driver, timeout)

    def load(self):
        """Open the landing page and wait until the login trigger is visible."""
        self.driver.get(self.base_url)
        self.wait.until(EC.presence_of_element_located(self.LOGIN_TRIGGER))
        return self

    def open_login_menu(self):
        """Click the login dropdown to reveal login options."""
        trigger = self.wait.until(EC.element_to_be_clickable(self.LOGIN_TRIGGER))
        trigger.click()
        return self

    def click_login_hudl(self):
        """Click the 'Log in to Hudl' link."""
        self.open_login_menu()
        link = self.wait.until(EC.element_to_be_clickable(self.HUDL_LOGIN_LINK))
        link.click()
        return self
