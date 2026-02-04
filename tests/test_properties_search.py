import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def test_properties_city_search(driver):
    wait = WebDriverWait(driver, 30)
    search_query = "Roswell"

    driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()
    
    wait.until(EC.url_contains("/s/"))

    properties_tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(., 'Properties')]")))
    properties_tab.click()
    wait.until(EC.visibility_of_element_located((By.XPATH, "//span[contains(text(), 'All Live Properties')]")))

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
    return findInShadow('input[name="Property__c-search-input"]');
    """
    search_input = driver.execute_script(find_script)
    assert search_input is not None, "Search box not found"

    search_input.click()
    search_input.send_keys(Keys.COMMAND + "a")
    search_input.send_keys(Keys.BACKSPACE)
    search_input.send_keys(search_query)
    
    driver.execute_script("""
        var input = arguments[0];
        input.dispatchEvent(new Event('input', { bubbles: true }));
        input.dispatchEvent(new Event('change', { bubbles: true }));
        var ev = new KeyboardEvent('keydown', { 'keyCode': 13, 'which': 13, 'key': 'Enter', 'bubbles': true });
        input.dispatchEvent(ev);
    """, search_input)

    # Allow time for the 51 rows to be filtered out
    time.sleep(5) 

    # Targeted locator for the City column value based on your HTML
    result_xpath = f"//td//span[contains(@class, 'uiOutputText') and @title='{search_query}']"
    
    try:
        target_record = wait.until(EC.presence_of_element_located((By.XPATH, result_xpath)))
        print(f"Success: Found {target_record.text} in the City column")
        assert search_query in target_record.text
    except Exception:
        rows = driver.find_elements(By.XPATH, "//table//tbody/tr")
        pytest.fail(f"Search failed. Record not found. Visible table rows: {len(rows)}")