import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_referrals_search_functionality(driver):
    """Verifies that a user can search for a specific referral record."""
    wait = WebDriverWait(driver, 30)
    search_query = "Uti Uti"

    # 1. Login
    driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()
    
    assert wait.until(EC.url_contains("/s/")), "Login failed!"

    # 2. Navigate to Referrals
    referrals_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Referrals & Campaign')]")))
    referrals_tab.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'Recently Viewed')]")))

    # 3. Locate Search Input via JavaScript (Shadow DOM handling)
    # Using your existing robust script
    find_script = """
    function findInShadow(selector, root = document) {
        let el = root.querySelector(selector);
        if (el) return el;
        let nodes = root.querySelectorAll('*');
        for (let node of nodes) {
            if (node.shadowRoot) {
                let found = findInShadow(selector, node.shadowRoot);
                if (found) return found;
            }
        }
        return null;
    }
    return findInShadow('input[name="Case-search-input"]');
    """
    search_input = driver.execute_script(find_script)
    
    # Assert existence instead of if/else
    assert search_input is not None, "Could not locate search box inside Shadow DOM"

    # 4. Perform Search
    search_input.click()
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.ENTER)

    # 5. Verification
    # Wait for table to refresh - using a specific wait is better than time.sleep
    result_xpath = f"//table//a[contains(text(), '{search_query}')]"
    
    try:
        target_record = wait.until(EC.presence_of_element_located((By.XPATH, result_xpath)))
        assert search_query in target_record.text, f"Expected {search_query} but found {target_record.text}"
    except Exception:
        # If it fails, we grab row count for the report
        rows = driver.find_elements(By.XPATH, "//table//tr")
        pytest.fail(f"Search failed. Visible table rows: {len(rows)}")