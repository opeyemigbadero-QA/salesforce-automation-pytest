import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# List views to be tested
LIST_VIEWS = [
    "All Live Properties",
    "All Properties",
    "Recently Viewed"
]

def test_properties_list(driver):
    """Verifies that all referral list views can be selected and loaded."""
    wait = WebDriverWait(driver, 30)

    # 1. Login
    driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()
    
    # Assert is better than print in pytest
    assert wait.until(EC.url_contains("/s/")), "Login failed: URL does not contain /s/"

    # 2. Navigate to Referrals
    properties_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Properties')]")))
    properties_tab.click()

    # 3. Loop through List Views
    for view_name in LIST_VIEWS:
        # Open Dropdown
        dropdown_trigger = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@title, 'Select a List View')]")))
        dropdown_trigger.click()
        
        # Select View
        view_item_xpath = f"//span[normalize-space()='{view_name}']"
        wait.until(EC.element_to_be_clickable((By.XPATH, view_item_xpath))).click()

        # Verify Header
        header_xpath = f"//span[contains(@class, 'slds-page-header__title') and normalize-space()='{view_name}']"
        header_visible = wait.until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
        
        # Assert the header matches the view selected
        assert header_visible.is_displayed(), f"Header for {view_name} was not displayed!"
        
        time.sleep(1) # Short pause for stability