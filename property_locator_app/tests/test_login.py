import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_login_verify_and_signout(pla_login):
    driver = pla_login
    wait = WebDriverWait(driver, 45)

    assert wait.until(EC.url_contains("properties-dev"))
    
    time.sleep(5)

    avatar_script = """
    function findInShadow(selector, root = document) {
        let el = root.querySelector(selector);
        if (el) return el;
        for (let node of root.querySelectorAll('*')) {
            if (node.shadowRoot) {
                let found = findInShadow(selector, node.shadowRoot);
                if (found) return found;
            }
        }
        return null;
    }
    return findInShadow("img[alt='User Avatar']");
    """

    avatar = wait.until(lambda d: d.execute_script(avatar_script))
    driver.execute_script("arguments[0].click();", avatar)

    sign_out_xpath = "//a[contains(., 'Sign Out') or contains(., 'Logout')]"
    sign_out = wait.until(EC.element_to_be_clickable((By.XPATH, sign_out_xpath)))
    driver.execute_script("arguments[0].click();", sign_out)

    assert wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Non-Profit Partner')]")))