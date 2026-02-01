
# Salesforce QA Automation Framework

A robust Selenium-based automation framework built with Python and Pytest. This suite validates critical workflows in Salesforce environments, including Referral list views, search functionality, and sequential dashboard reporting.

## Technical Stack
* **Language:** Python 3.14
* **Testing Framework:** Pytest 9.0
* **Automation Tool:** Selenium WebDriver
* **Driver Management:** Webdriver-Manager
* **Reporting:** Pytest-HTML

## Framework Highlights
* **Stale Element Protection:** Implements a robust retry logic and frame-switching strategy to handle Salesforce's dynamic DOM updates.
* **Shadow DOM Navigation:** Utilizes custom JavaScript injection to interact with elements inside Salesforce's nested Shadow DOM components.
* **Fixture-Based Architecture:** Uses `conftest.py` for global WebDriver management, ensuring clean setup and teardown for every test.
* **Scalable reporting:** Integrated HTML reporting with failure diagnostics.

## Project Structure
* `tests/`: Directory containing all automation test scripts.
* `conftest.py`: Global configuration and WebDriver fixtures.
* `requirements.txt`: Python dependencies and version locking.
* `.gitignore`: Excludes environment-specific files and sensitive reports.

