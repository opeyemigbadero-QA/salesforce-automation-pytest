import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException
import time

def test_run_salesforce_report_suite(driver):
    """Verifies all reports in a single sequential suite with multi-layer stale protection."""
    wait = WebDriverWait(driver, 30)

    reports_to_test = [
        {"link": "Total Agency Referrals Submitted", "title": "Total Agency Referrals Submitted"},
        {"link": "Total Agency Housed", "title": "Total Agency Housed"},
        {"link": "Total Individuals Housed", "title": "Total Individuals Housed"},
        {"link": "Total Agency Open Referrals", "title": "Total Agency Open Referrals"},
        {"link": "Total Individual Open Referrals", "title": "Total Individual Open Referrals"},
        {"link": "Break Open Referrals down by status", "title": "Break Open Referrals down by status"}
    ]

    # ---------- LOGIN ----------
    driver.get("https://opendoors--qa.sandbox.my.site.com/s/login/")
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input.input"))).send_keys("udeme@opendoorsatl.org.qa.casemanager")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='password']"))).send_keys("14Gconnect#1")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'loginButton')]"))).click()
    
    assert wait.until(EC.url_contains("/s/")), "Login failed"

    for report in reports_to_test:
        # --- STEP 1: ROBUST FRAME SWITCH ---
        driver.switch_to.default_content()
        
        # We wrap the iframe switch in a retry loop to catch staleness at the switch moment
        for attempt in range(3):
            try:
                dashboard_frame = wait.until(
                    EC.presence_of_element_located((By.XPATH, "//iframe[contains(@title, 'dashboard')] | //iframe"))
                )
                driver.switch_to.frame(dashboard_frame)
                break # Success!
            except StaleElementReferenceException:
                if attempt == 2: raise # Re-throw if it fails 3 times
                time.sleep(2) # Wait for Salesforce to finish re-painting the DOM
                continue

        # --- STEP 2: ROBUST LINK CLICK ---
        link_xpath = f"//a[contains(., '{report['link']}')]"
        click_attempts = 0
        while click_attempts < 2:
            try:
                report_link = wait.until(EC.element_to_be_clickable((By.XPATH, link_xpath)))
                driver.execute_script("arguments[0].click();", report_link)
                break
            except StaleElementReferenceException:
                click_attempts += 1
                time.sleep(1)
        
        driver.switch_to.default_content()
        time.sleep(3) 

        # --- STEP 3: MULTI-LAYER VERIFICATION ---
        header_found = False
        header_xpath = f"//span[@title='{report['title']}']"

        try:
            # Check Main Page first
            wait.until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
            header_found = True
        except:
            # Fallback: Scan Iframes
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            for frame in iframes:
                driver.switch_to.default_content()
                driver.switch_to.frame(frame)
                try:
                    WebDriverWait(driver, 5).until(EC.visibility_of_element_located((By.XPATH, header_xpath)))
                    header_found = True
                    break 
                except:
                    continue
        
        assert header_found, f"Failed to find header for: {report['title']}"

        # --- STEP 4: NAVIGATE BACK & SETTLE ---
        driver.switch_to.default_content()
        driver.back()
        
        # Crucial: Salesforce sandboxes need time to re-initialize the dashboard after 'back'
        # If we loop too fast, Step 1 will catch a 'stale' dashboard frame from the previous page
        time.sleep(6)