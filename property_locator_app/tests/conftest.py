import os
import pytest
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
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

    non_profit_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(., 'Non-Profit Partner')]")))
    non_profit_button.click()

    user_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='username'], input[placeholder*='Username']")))
    user_field.send_keys(username)

    pass_field = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "input[name='password'], input[placeholder*='Password']")))
    pass_field.send_keys(password)

    
    pass_field.send_keys(Keys.RETURN)
    print("Login initiated via Return key")

   
    wait.until(EC.url_contains("/s/"))
    print("Login successful - Session established")
    
    return driver