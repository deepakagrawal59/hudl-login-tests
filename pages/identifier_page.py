from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class IdentifierPage:
    EMAIL_INPUT = (By.ID, "username")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    ACTIVE_ERROR = (By.CSS_SELECTOR, ".ulp-error-info[data-is-error='true']")

    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def enter_email(self, email):
        field = self.wait.until(EC.visibility_of_element_located(self.EMAIL_INPUT))
        field.clear()
        field.send_keys(email)
        return self

    def click_continue(self):
        btn = self.wait.until(EC.element_to_be_clickable(self.CONTINUE_BUTTON))
        btn.click()
        return self

    def get_active_error_message(self):
        try:
            error_elem = self.wait.until(
                EC.visibility_of_element_located(self.ACTIVE_ERROR)
            )
            return error_elem.text.strip()
        except (TimeoutException, NoSuchElementException):
            return ""
