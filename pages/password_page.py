# pages/password_page.py
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class PasswordPage:
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    FORGOT_PASSWORD_LINK = (By.CSS_SELECTOR, "a[href*='password-reset-start']")

    ERROR_ANY = (
        By.CSS_SELECTOR,
        "#error-element-password.ulp-input-error-message, "
        "#error-cs-password-required.ulp-error-info[data-is-error='true']",
    )

    RESET_TITLE = (By.XPATH, "//h1[normalize-space()='Reset Password']")
    RESET_DESCRIPTION = (By.ID, "aria-description-text")
    RESET_EMAIL_INPUT = (By.ID, "email")
    RESET_CONTINUE_BUTTON = (
        By.CSS_SELECTOR,
        "button[data-action-button-primary='true']",
    )

    def __init__(self, driver, timeout=20):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)

    def enter_password(self, password: str):
        field = self.wait.until(EC.visibility_of_element_located(self.PASSWORD_INPUT))
        field.clear()
        field.send_keys(password)
        return self

    def click_login(self):
        self.wait.until(EC.element_to_be_clickable(self.LOGIN_BUTTON)).click()
        return self

    def click_forgot_password(self):
        self.wait.until(EC.element_to_be_clickable(self.FORGOT_PASSWORD_LINK)).click()
        return self

    def get_active_error_message(self) -> str:

        def _error_with_text(driver):
            try:
                el = driver.find_element(*self.ERROR_ANY)
                txt = (el.text or "").strip()
                return el if txt else None
            except (TimeoutException, NoSuchElementException):
                return None

        el = WebDriverWait(self.driver, 15).until(_error_with_text)
        return el.text.strip()

    def is_password_field_in_error_state(self) -> bool:
        field = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        aria_invalid = (field.get_attribute("aria-invalid") or "").lower() == "true"
        try:
            err = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.ERROR_ANY)
            )
            return aria_invalid and err.is_displayed()
        except Exception:
            return False

    def is_password_masked(self) -> bool:
        field = self.wait.until(EC.presence_of_element_located(self.PASSWORD_INPUT))
        return (field.get_attribute("type") or "").lower() == "password"

    def wait_for_reset_password_page(self):
        self.wait.until(EC.visibility_of_element_located(self.RESET_TITLE))
        return self

    def get_prefilled_email(self) -> str:
        el = self.wait.until(EC.presence_of_element_located(self.RESET_EMAIL_INPUT))
        return (el.get_attribute("value") or "").strip()

    def is_reset_ui_complete(self) -> bool:
        title_visible = self.wait.until(
            EC.visibility_of_element_located(self.RESET_TITLE)
        ).is_displayed()
        desc_visible = self.wait.until(
            EC.visibility_of_element_located(self.RESET_DESCRIPTION)
        ).is_displayed()
        btn_visible = self.wait.until(
            EC.visibility_of_element_located(self.RESET_CONTINUE_BUTTON)
        ).is_displayed()
        return title_visible and desc_visible and btn_visible
