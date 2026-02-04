import os
import pytest
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

load_dotenv()

@pytest.fixture(scope="function")
def pla_login(driver):
    wait = WebDriverWait(driver, 40)
    
    url = os.getenv("PLA_URL")
    username = os.getenv("PLA_USERNAME")
    password = os.getenv("PLA_PASSWORD")

    driver.get(url)

    non_profit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Enter as a Non-Profit Partner')]")))
    non_profit_button.click()

    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Username' or @name='username']"))).send_keys(username)
    wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Password' or @name='password']"))).send_keys(password)
    
    login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class, 'slds-button') and contains(., 'Log in')] | //button[@type='button' and contains(., 'Log in')]")))
    driver.execute_script("arguments[0].click();", login_button)
    
    return driver