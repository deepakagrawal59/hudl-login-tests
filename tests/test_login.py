import logging
import os

import pytest
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.identifier_page import IdentifierPage
from pages.landing_page import LandingPage
from pages.password_page import PasswordPage

logger = logging.getLogger(__name__)

load_dotenv()
BASE_URL = os.getenv("BASE_URL", "https://www.hudl.com/")
HUDL_EMAIL = os.getenv("HUDL_EMAIL")
HUDL_PASSWORD = os.getenv("HUDL_PASSWORD")


@pytest.mark.login
def test_valid_login(driver):
    logger.info("Starting: Valid login test")
    LandingPage(driver, BASE_URL).load().click_login_hudl()

    logger.info(f"Entering email: {HUDL_EMAIL}")
    IdentifierPage(driver).enter_email(HUDL_EMAIL).click_continue()

    logger.info("Entering password (masked)")
    PasswordPage(driver).enter_password(HUDL_PASSWORD)
    assert PasswordPage(driver).is_password_masked()
    PasswordPage(driver).click_login()

    logger.info("Verifying successful login")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".hui-globalnav__group a[data-qa-id='webnav-globalnav-home']",
            )
        )
    )
    assert (
        "/home" in driver.current_url.lower()
        or "dashboard" in driver.current_url.lower()
    )
    logger.info("Valid login successful")


@pytest.mark.login
@pytest.mark.parametrize(
    "invalid_email,expected_error",
    [
        ("", "Enter an email address"),
        ("invalid@", "Enter a valid email."),
        ("user@@domain.com", "Enter a valid email."),
        ("user!@domain", "Enter a valid email."),
    ],
)
def test_invalid_email_errors(driver, invalid_email, expected_error):
    logger.info(f"Testing invalid email: {invalid_email}")
    LandingPage(driver, BASE_URL).load().click_login_hudl()
    IdentifierPage(driver).enter_email(invalid_email).click_continue()

    active_error = IdentifierPage(driver).get_active_error_message()
    logger.info(f"Expected: '{expected_error}', Got: '{active_error}'")
    assert expected_error == active_error
    logger.info("Invalid email error validated")


@pytest.mark.login
def test_wrong_password(driver):
    logger.info("Testing wrong password scenario")
    LandingPage(driver, BASE_URL).load().click_login_hudl()
    IdentifierPage(driver).enter_email(HUDL_EMAIL).click_continue()

    pwd = PasswordPage(driver)
    pwd.enter_password("WrongPassword123").click_login()

    error = pwd.get_active_error_message()
    logger.info(
        f"Expected: 'Your email or password is incorrect. Try again.', Got: '{error}'"
    )
    assert error == "Your email or password is incorrect. Try again."

    logger.info("Validating red error highlight on password field")
    assert pwd.is_password_field_in_error_state()
    logger.info("Wrong password error validated")


@pytest.mark.login
def test_missing_password(driver):
    logger.info("Testing missing password scenario")
    LandingPage(driver, BASE_URL).load().click_login_hudl()
    IdentifierPage(driver).enter_email(HUDL_EMAIL).click_continue()

    PasswordPage(driver).click_login()
    error = PasswordPage(driver).get_active_error_message()
    logger.info(f"Expected: 'Enter your password' in '{error}'")
    assert "Enter your password." == error
    logger.info("Missing password error validated")


@pytest.mark.session
def test_session_persistence(driver):
    logger.info("Testing session persistence after login")
    LandingPage(driver, BASE_URL).load().click_login_hudl()
    IdentifierPage(driver).enter_email(HUDL_EMAIL).click_continue()
    PasswordPage(driver).enter_password(HUDL_PASSWORD).click_login()

    logger.info("Revisiting home page to check session persistence")
    driver.get(f"{BASE_URL}/home")
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                ".hui-globalnav__group a[data-qa-id='webnav-globalnav-home']",
            )
        )
    )
    assert "/home" in driver.current_url.lower()
    logger.info("Session persistence validated")


@pytest.mark.logout
def test_logout(driver):
    logger.info("Testing logout flow")
    LandingPage(driver, BASE_URL).load().click_login_hudl()
    IdentifierPage(driver).enter_email(HUDL_EMAIL).click_continue()
    PasswordPage(driver).enter_password(HUDL_PASSWORD).click_login()

    logger.info("Clicking user menu")
    user_menu = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, ".hui-globaluseritem__display-name")
        )
    )
    user_menu.click()

    logger.info("Clicking logout link")
    logout_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "a[data-qa-id='webnav-usermenu-logout']")
        )
    )
    logout_link.click()

    logger.info("Validating we have left /home")
    WebDriverWait(driver, 10).until_not(EC.url_contains("/home"))
    assert "home" not in driver.current_url.lower()
    LandingPage(driver, BASE_URL).load()
    assert "home" not in driver.current_url.lower()
    logger.info("Logout flow validated")


@pytest.mark.resetpw
def test_reset_password_ui(driver):
    """Validate Reset Password page UI and pre-filled email."""
    LandingPage(driver, BASE_URL).load().click_login_hudl()
    IdentifierPage(driver).enter_email(HUDL_EMAIL).click_continue()
    pwd_page = PasswordPage(driver)
    pwd_page.click_forgot_password().wait_for_reset_password_page()
    assert pwd_page.is_reset_ui_complete(), "Reset password UI elements missing"
    assert pwd_page.get_prefilled_email() == HUDL_EMAIL
