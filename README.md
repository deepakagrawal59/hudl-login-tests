# Hudl Login Test Suite

Automated test suite for validating **Hudl's login and session flows** using **Selenium WebDriver** and **pytest**.

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Create `.env` file** with your test credentials:

   ```env
   HUDL_BASE_URL=https://www.hudl.com/
   HUDL_EMAIL=your-test-email@example.com
   HUDL_PASSWORD=your-test-password
   ```

---


### Run all tests

```bash
pytest
```

### Run by category

```bash
pytest -m login     # Login flow tests
pytest -m session   # Session persistence tests
pytest -m logout    # Logout flow tests
pytest -m resetpw   # Password reset UI tests
```

---

## Test Categories

* **Login Tests**
  Valid login, invalid emails, wrong passwords, missing passwords.

* **Session Tests**
  Validates session persistence after login.

* **Logout Tests**
  Validates complete logout flow and ensures session is cleared.

* **Reset Password Tests**
  Validates reset password page UI, pre-filled email, and elements.

---
