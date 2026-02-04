import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_verify_and_signout(pla_login):
    driver = pla_login
    wait = WebDriverWait(driver, 45)

    
    wait.until(lambda d: "properties" in d.current_url.lower())
    print("Navigated to Properties-Dev page")
    
   
    avatar_button = wait.until(EC.element_to_be_clickable((By.ID, "popover-platform")))
    driver.execute_script("arguments[0].click();", avatar_button)
    print("Profile menu opened")

    
    sign_out_btn = wait.until(EC.element_to_be_clickable((By.ID, "salesforce-logout")))
    driver.execute_script("arguments[0].click();", sign_out_btn)
    print("Sign Out clicked")

   
    landing_page_check = "//button[contains(., 'Non-Profit Partner')]"
    assert wait.until(EC.presence_of_element_located((By.XPATH, landing_page_check)))
    print("Logout successful - Returned to landing page")